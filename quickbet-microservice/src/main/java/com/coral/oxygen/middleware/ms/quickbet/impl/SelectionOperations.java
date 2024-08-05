package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.*;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.OveraskReadBetExecutionService;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.ComplexSelection;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.AddComplexSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.AddSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.ComplexSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.RemoveComplexSelectionRequest;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuildResponseModel;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.OutcomeDetails;
import io.vavr.Tuple;
import io.vavr.Tuple3;
import io.vavr.collection.HashSet;
import io.vavr.collection.List;
import io.vavr.collection.Map;
import io.vavr.collection.Set;
import io.vavr.control.Option;
import java.util.UUID;
import java.util.function.Function;
import lombok.RequiredArgsConstructor;
import org.apache.commons.lang3.StringUtils;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class SelectionOperations {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private static final String ERROR_READING_OUTCOME_DATA = "Error reading outcome data.";
  static final String EMPTY_JSON_RESPONSE = "{}";
  private final BuildBetOperations buildBetOperations;
  private final OveraskReadBetExecutionService overaskReadBetExecutionService;
  private final LiveServService liveServService;
  private final SiteServerService siteServerService;

  public void addSelection(Session session, AddSelectionRequest request) {
    if (validateAddSelection(session, request)) {
      session.addSelection(request.getOutcomeId());
      fetchOutcomesEventsForSelections(session).forEach(session::addOutcomeEvent);
      BetBuildResponseModel betBuildResponseModel = buildBetOperations.buildBet(session);
      subscribeToChannels(session, betBuildResponseModel);
    }
  }

  private boolean validateAddSelection(Session session, AddSelectionRequest request) {
    if (isOutcomeIdEmpty(request) || session.isOutcomeIdPresent(request.getOutcomeId())) {
      ASYNC_LOGGER.info(
          "Skipping selection addition as requested outcome id: {}, have been already added",
          request.getOutcomeId());

      session.sendData(SELECTION_EMPTY_OR_ALREADY_ADDED.code(), EMPTY_JSON_RESPONSE);
      return false;
    }
    return true;
  }

  public void removeSelection(Session session, String outcomeId) {
    if (validateRemoveSelection(session, outcomeId)) {
      session.removeSelectionByOutcomeId(outcomeId);
      session.removeOutcomeEvent(outcomeId);
      session.unsubscribeFromOutcomesIdsRooms(List.of(outcomeId));
      BetBuildResponseModel betBuildResponseModel = buildBetOperations.buildBet(session);
      subscribeToChannels(session, betBuildResponseModel);
    }
  }

  private boolean validateRemoveSelection(Session session, String outcomeId) {
    if (!session.isOutcomeIdPresent(outcomeId)) {
      ASYNC_LOGGER.info(
          "Skipping selection removal for outcomeId: {}, as it is not present", outcomeId);
      session.sendData(SELECTION_TO_REMOVE_NOT_PRESENT.code(), EMPTY_JSON_RESPONSE);
      return false;
    }
    return true;
  }

  private boolean isOutcomeIdEmpty(AddSelectionRequest request) {
    return StringUtils.isEmpty(request.getOutcomeId());
  }

  public void addComplexSelection(Session session, AddComplexSelectionRequest request) {
    ComplexSelection complexSelection = complexSelectionRequestToSelection(request);
    if (validateAddComplexSelection(session, complexSelection)) {
      session.addComplexSelections(complexSelection);
      fetchOutcomesEventsForSelections(session).forEach(session::addOutcomeEvent);
      BetBuildResponseModel betBuildResponseModel = buildBetOperations.buildBet(session);
      subscribeToChannels(session, betBuildResponseModel);
    }
  }

  public boolean validateAddComplexSelection(Session session, ComplexSelection complexSelection) {
    if (isComplexSelectionAlreadyPresent(session, complexSelection)) {
      ASYNC_LOGGER.info(
          "Skipping selection addition as requested selection: {}, have been already added",
          complexSelection);
      session.sendData(SELECTION_EMPTY_OR_ALREADY_ADDED.code(), EMPTY_JSON_RESPONSE);
      return false;
    }
    return true;
  }

  public void removeComplexSelection(Session session, RemoveComplexSelectionRequest request) {
    ComplexSelection complexSelection = complexSelectionRequestToSelection(request);
    if (validateRemoveComplexSelection(session, complexSelection)) {
      session.removeComplexSelection(complexSelection);
      session.removeOutcomesEvents(request.getOutcomeIds());
      session.unsubscribeFromOutcomesIdsRooms(request.getOutcomeIds());
      BetBuildResponseModel betBuildResponseModel = buildBetOperations.buildBet(session);
      subscribeToChannels(session, betBuildResponseModel);
    }
  }

  public boolean validateRemoveComplexSelection(
      Session session, ComplexSelection complexSelection) {
    if (!isComplexSelectionAlreadyPresent(session, complexSelection)) {
      ASYNC_LOGGER.info(
          "Skipping complex selection removal for selection: {}, as it is not present",
          complexSelection);
      session.sendData(SELECTION_TO_REMOVE_NOT_PRESENT.code(), EMPTY_JSON_RESPONSE);
      return false;
    }
    return true;
  }

  private boolean isComplexSelectionAlreadyPresent(
      Session session, ComplexSelection complexSelection) {
    return session.getComplexSelections().contains(complexSelection);
  }

  private ComplexSelection complexSelectionRequestToSelection(
      ComplexSelectionRequest selectionRequest) {
    return new ComplexSelection(
        selectionRequest.getSelectionType(), selectionRequest.getOutcomeIds());
  }

  private Map<String, Event> fetchOutcomesEventsForSelections(Session session) {
    List<String> allSelectedOutcomeIds = getAllSelectedOutcomeIds(session);
    List<String> outcomeIdsToBeRequested =
        allSelectedOutcomeIds.filter(id -> session.getOutcomeEvent(id).isEmpty());

    List<Event> outcomesEvents = siteServerService.getEventsForOutcomeIds(outcomeIdsToBeRequested);

    return outcomeIdsToBeRequested.toMap(
        Function.identity(),
        outcomeId ->
            extractEvent(outcomesEvents, outcomeId)
                .getOrElseThrow(() -> getSiteServException(outcomeId)));
  }

  private List<String> getAllSelectedOutcomeIds(Session session) {
    List<String> regularSelections = session.getSelectedOutcomeIds();
    List<ComplexSelection> complexSelections = session.getComplexSelections();

    return regularSelections.prependAll(complexSelections.flatMap(ComplexSelection::getOutcomeIds));
  }

  private SiteServException getSiteServException(String outcomeId) {
    return new SiteServException(
        REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
        EVENT_NOT_FOUND.code(),
        ERROR_READING_OUTCOME_DATA + " Data not found. OutcomeIds - " + outcomeId);
  }

  private Option<Event> extractEvent(List<Event> events, String outcomeId) {
    return events.filter(event -> isOutcomeIdMatchingEvent(outcomeId, event)).headOption();
  }

  private boolean isOutcomeIdMatchingEvent(String outcomeId, Event event) {
    return event.getChildren().stream()
        .anyMatch(
            children ->
                children.getMarket().getOutcomes().stream()
                    .anyMatch(outcome -> outcome.getId().equals(outcomeId)));
  }

  private Tuple3<String, Event, Market> outcomeEventMarketToTuple(
      String outcomeId, Event event, Market market) {
    return Tuple.of(outcomeId, event, market);
  }

  public void restoreState(Session session, String bppToken) {
    if (!session.getSelectedOutcomeIds().isEmpty() || !session.getComplexSelections().isEmpty()) {
      fetchOutcomesEventsForSelections(session).forEach(session::addOutcomeEvent);
      BetBuildResponseModel betBuildResponseModel = buildBetOperations.buildBet(session);
      subscribeToChannels(session, betBuildResponseModel);
    }
    if (StringUtils.isNotEmpty(bppToken) && !session.getBetsToReadInBackground().isEmpty()) {
      restoreBetReadsInBackground(session, bppToken);
    }
  }

  private void restoreBetReadsInBackground(Session session, String bppToken) {
    Map<UUID, List<BetRef>> betsToReadInBackground = session.getBetsToReadInBackground();
    session.clearAllTasks();
    session.save();
    betsToReadInBackground.forEach(
        entry -> overaskReadBetExecutionService.scheduleReadBet(session, entry._2, bppToken));
  }

  private void subscribeToChannels(Session session, BetBuildResponseModel betBuildResponseModel) {
    Map<String, Set<String>> channelsToSubscribeForOutcomeId =
        calculateLiveServChannels(betBuildResponseModel);
    subscribeToChannels(session, channelsToSubscribeForOutcomeId);
  }

  private void subscribeToChannels(
      Session session, Map<String, Set<String>> channelsToSubscribeForOutcomeId) {
    Set<String> channelsToSubscribe =
        channelsToSubscribeForOutcomeId.flatMap(entry -> entry._2).toSet();

    channelsToSubscribe.forEach(liveServService::subscribe);
    session.subscribeToRooms(channelsToSubscribeForOutcomeId);
  }

  private Map<String, Set<String>> calculateLiveServChannels(
      BetBuildResponseModel betBuildResponseModel) {

    return List.ofAll(betBuildResponseModel.getOutcomeDetails())
        .toMap(OutcomeDetails::getId, this::calculateLiveServChannels);
  }

  private Set<String> calculateLiveServChannels(OutcomeDetails outcomeDetails) {
    return HashSet.ofAll(
        LiveServChannelUtils.calculateLiveServChannels(
            outcomeDetails.getId(), outcomeDetails.getMarketId(), outcomeDetails.getEventId()));
  }

  public void clearSelection(Session session) {
    session.clearAllSelections();
    session.save();
    session.sendData(CLEAR_SELECTION_RESPONSE_CODE.code(), new Object());
  }
}
