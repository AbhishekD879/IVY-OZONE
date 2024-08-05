package com.coral.oxygen.middleware.ms.quickbet;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.ComplexSelection;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachSelectionRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.CalculateOddsRequestDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.FreeBetForChannelRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.RegularSelectionResponse;
import com.coral.oxygen.middleware.ms.quickbet.impl.SessionStorage;
import com.egalacoral.spark.siteserver.model.Event;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuildResponseModel;
import io.vavr.collection.HashMap;
import io.vavr.collection.HashSet;
import io.vavr.collection.List;
import io.vavr.collection.Map;
import io.vavr.collection.Set;
import io.vavr.control.Option;
import java.util.Collection;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.Future;
import java.util.function.Function;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.util.Assert;

public class BaseSession implements Session {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  private static final String ALL_OUTCOMES_IDS = "ALL";
  private final SessionStorage<SessionDto> sessionStorage;
  private SessionDto sessionDto;
  private SessionListener listener;
  private RegularSelectionResponse selectionResponse;

  private Map<String, Set<String>> subscriptionsForOutcomeId = HashMap.empty();
  private BetBuildResponseModel betBuildResponseModel;
  private Map<String, Event> outcomeEventsMap = HashMap.empty();
  private ConcurrentMap<UUID, Future> tasks = new ConcurrentHashMap<>();

  public BaseSession(String sessionId, SessionStorage<SessionDto> sessionStorage) {
    this(new SessionDto(sessionId), sessionStorage);
  }

  private BaseSession(SessionDto sessionDto, SessionStorage<SessionDto> sessionStorage) {
    Assert.notNull(sessionDto, "sessionDto cannot be null");
    Assert.notNull(sessionDto.getSessionId(), "sessionId cannot be null");
    Assert.notNull(sessionStorage, "sessionStorage cannot be null");
    this.sessionDto = sessionDto;
    this.sessionStorage = sessionStorage;
  }

  @Override
  public String sessionId() {
    return sessionDto.getSessionId();
  }

  @Override
  public void setListener(SessionListener listener) {
    this.listener = listener;
  }

  public SessionDto sessionDto() {
    return sessionDto;
  }

  /**
   * Save in session information about subscribed channels passed as a parameter. This method put
   * all channels into one category and there is no information kept which outcomeId uses which
   * channels.
   *
   * @deprecated please use {@link #subscribeToRooms(Map)} method
   */
  @Deprecated(forRemoval = false)
  @Override
  public void subscribeToRooms(Collection<String> rooms) {
    subscribeToRooms(HashMap.of(ALL_OUTCOMES_IDS, HashSet.ofAll(rooms)));
  }

  /**
   * Save subscriptions in this session and send them to the client.
   *
   * @param channelsToSubscribeForOutcomeId map with outcomeId and related to it list of channels to
   *     subscribe
   */
  @Override
  public void subscribeToRooms(Map<String, Set<String>> channelsToSubscribeForOutcomeId) {
    addChannelsToSubscribe(channelsToSubscribeForOutcomeId);
    listener.subscribeToRooms(getUniqueSubscribedChannels().toJavaSet());
  }

  @Override
  public void unsubscribeFromAllRooms() {
    listener.unsubscribeFromRooms(getUniqueSubscribedChannels().toJavaSet());
    subscriptionsForOutcomeId = HashMap.empty();
  }

  @Override
  public void unsubscribeFromOutcomesIdsRooms(List<String> outcomeIds) {
    Set<String> previousSubscriptions = getUniqueSubscribedChannels();
    subscriptionsForOutcomeId = subscriptionsForOutcomeId.removeAll(outcomeIds);
    Set<String> leftSubscriptions = getUniqueSubscribedChannels();
    Set<String> removedSubscriptions = previousSubscriptions.removeAll(leftSubscriptions);
    if (removedSubscriptions.nonEmpty()) {
      listener.unsubscribeFromRooms(removedSubscriptions.toJavaSet());
    }
  }

  private void addChannelsToSubscribe(Map<String, Set<String>> channelsToSubscribeForOutcomeId) {
    subscriptionsForOutcomeId = channelsToSubscribeForOutcomeId.merge(subscriptionsForOutcomeId);
  }

  private Set<String> getUniqueSubscribedChannels() {
    return subscriptionsForOutcomeId.values().flatMap(Function.identity()).toSet();
  }

  @Override
  public boolean exists() {
    return this.sessionStorage.find(this.sessionDto.getSessionId()).isPresent();
  }

  @Override
  public boolean fetch() {
    Optional<SessionDto> fetchedSessionDto = this.sessionStorage.find(sessionDto.getSessionId());
    if (fetchedSessionDto.isPresent()) {
      this.sessionDto = fetchedSessionDto.get();
      return true;
    } else {
      return false;
    }
  }

  @Override
  public void save() {
    this.sessionStorage.persist(sessionDto);
  }

  @Override
  public RegularSelectionResponse getRegularSelectionResponse() {
    return selectionResponse;
  }

  @Override
  public void setRegularSelectionResponse(RegularSelectionResponse selectionResponse) {
    this.selectionResponse = selectionResponse;
  }

  @Override
  public void clearRegularSelection() {
    sessionDto.setRegularSelectionRequest(null);
    selectionResponse = null;
  }

  @Override
  public FreeBetForChannelRequestData getFreeBetForChannelRequestData() {
    return sessionDto.getFreeBetForChannelRequestData();
  }

  @Override
  public void setFreeBetForChannelRequestData(FreeBetForChannelRequestData request) {
    sessionDto.setFreeBetForChannelRequestData(request);
  }

  @Override
  public void removeSelectionByOutcomeId(String outcomeId) {
    sessionDto.setSelectedOutcomeIds(sessionDto.getSelectedOutcomeIds().remove(outcomeId));
  }

  @Override
  public void addSelection(String outcomeId) {
    sessionDto.setSelectedOutcomeIds(sessionDto.getSelectedOutcomeIds().append(outcomeId));
  }

  @Override
  public void removeComplexSelection(ComplexSelection selection) {
    List<ComplexSelection> afterRemoval = sessionDto.getComplexSelections().removeAll(selection);
    sessionDto.setComplexSelections(afterRemoval);
  }

  @Override
  public void addComplexSelections(ComplexSelection selection) {
    List<ComplexSelection> afterAdding = sessionDto.getComplexSelections().append(selection);
    sessionDto.setComplexSelections(afterAdding);
  }

  @Override
  public void setBetBuildResponse(BetBuildResponseModel betBuildResponseModel) {
    this.betBuildResponseModel = betBuildResponseModel;
  }

  @Override
  public void setSelectedOutcomeIds(List<String> outcomes) {
    sessionDto.setSelectedOutcomeIds(outcomes);
  }

  @Override
  public boolean isOutcomeIdPresent(String outcomeId) {
    return getSelectedOutcomeIds().contains(outcomeId);
  }

  @Override
  public void setComplexSelections(List<ComplexSelection> selections) {
    sessionDto.setComplexSelections(selections);
  }

  @Override
  public List<String> getSelectedOutcomeIds() {
    return sessionDto.getSelectedOutcomeIds();
  }

  @Override
  public void clearAllSelections() {
    sessionDto.setSelectedOutcomeIds(List.empty());
    sessionDto.setComplexSelections(List.empty());
    this.clearRegularSelection();
    this.unsubscribeFromAllRooms();
  }

  @Override
  public List<ComplexSelection> getComplexSelections() {
    return sessionDto.getComplexSelections();
  }

  @Override
  public BetBuildResponseModel getBetBuildResponseModel() {
    return betBuildResponseModel;
  }

  @Override
  public List<CalculateOddsRequestDto> getOddsRequest() {
    return sessionDto.getOddsRequest();
  }

  @Override
  public void setOddsRequest(List<CalculateOddsRequestDto> oddsRequest) {
    sessionDto.setOddsRequest(oddsRequest);
  }

  @Override
  public BanachSelectionRequestData getBanachSelectionData() {
    return sessionDto.getBanachSelectionRequestData();
  }

  @Override
  public void setBanachSelectionData(BanachSelectionRequestData selectionData) {
    sessionDto.setBanachSelectionRequestData(selectionData);
  }

  @Override
  public void sendData(String message, Object data) {
    listener.sendData(message, data);
  }

  @Override
  public RegularSelectionRequest getRegularSelectionRequest() {
    return sessionDto.getRegularSelectionRequest();
  }

  @Override
  public void setRegularSelectionRequest(RegularSelectionRequest request) {
    sessionDto.setRegularSelectionRequest(request);
  }

  @Override
  public void setToken(String token) {
    sessionDto.setToken(token);
  }

  @Override
  public String getToken() {
    return sessionDto.getToken();
  }

  @Override
  public void addOutcomeEvent(String outcomeId, Event event) {
    outcomeEventsMap = outcomeEventsMap.put(outcomeId, event);
  }

  @Override
  public Option<Event> getOutcomeEvent(String outcomeId) {
    return outcomeEventsMap.get(outcomeId);
  }

  @Override
  public void removeOutcomeEvent(String outcomeId) {
    outcomeEventsMap = outcomeEventsMap.remove(outcomeId);
  }

  @Override
  public void removeOutcomesEvents(List<String> outcomeIds) {
    outcomeEventsMap = outcomeEventsMap.removeAll(outcomeIds);
  }

  @Override
  public void registerPendingTask(
      UUID uuid, Future futureTask, List<BetRef> betsToReadInBackground) {
    sessionDto.setBetsToReadInBackground(
        sessionDto.getBetsToReadInBackground().put(uuid, betsToReadInBackground));
    tasks.put(uuid, futureTask);
  }

  @Override
  public void finishTask(UUID uuid) {
    ASYNC_LOGGER.info(String.format("Finishing task with id %s for session %s", uuid, sessionId()));
    tasks.remove(uuid).cancel(true);
  }

  @Override
  public void finishTasks() {
    tasks.keySet().forEach(this::finishTask);
  }

  @Override
  public io.vavr.collection.Map<UUID, List<BetRef>> getBetsToReadInBackground() {
    return sessionDto.getBetsToReadInBackground();
  }

  @Override
  public void clearAllTasks() {
    sessionDto.setBetsToReadInBackground(io.vavr.collection.HashMap.empty());
  }

  @Override
  public String toString() {
    return "Session{"
        + "sessionStorage="
        + sessionStorage
        + ", sessionDto="
        + sessionDto
        + ", listener="
        + listener
        + ", subscriptionsForOutcomeId="
        + subscriptionsForOutcomeId
        + '}';
  }
}
