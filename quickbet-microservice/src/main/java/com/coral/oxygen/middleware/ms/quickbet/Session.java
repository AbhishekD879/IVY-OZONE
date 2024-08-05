package com.coral.oxygen.middleware.ms.quickbet;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.ComplexSelection;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachSelectionRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.CalculateOddsRequestDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.FreeBetForChannelRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.RegularSelectionResponse;
import com.egalacoral.spark.siteserver.model.Event;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuildResponseModel;
import io.vavr.collection.List;
import io.vavr.collection.Map;
import io.vavr.collection.Set;
import io.vavr.control.Option;
import java.util.Collection;
import java.util.UUID;
import java.util.concurrent.Future;

public interface Session {

  String sessionId();

  void setListener(SessionListener listener);

  void subscribeToRooms(Collection<String> rooms);

  void subscribeToRooms(Map<String, Set<String>> roomsForOutcomeId);

  void unsubscribeFromOutcomesIdsRooms(List<String> outcomeIds);

  void unsubscribeFromAllRooms();

  boolean exists();

  boolean fetch();

  void save();

  List<String> getSelectedOutcomeIds();

  List<ComplexSelection> getComplexSelections();

  BetBuildResponseModel getBetBuildResponseModel();

  List<CalculateOddsRequestDto> getOddsRequest();

  void setOddsRequest(List<CalculateOddsRequestDto> oddsRequest);

  BanachSelectionRequestData getBanachSelectionData();

  void setBanachSelectionData(BanachSelectionRequestData selectionData);

  void sendData(String message, Object data);

  RegularSelectionRequest getRegularSelectionRequest();

  void setRegularSelectionRequest(RegularSelectionRequest request);

  RegularSelectionResponse getRegularSelectionResponse();

  void setRegularSelectionResponse(RegularSelectionResponse selectionResponse);

  void clearRegularSelection();

  FreeBetForChannelRequestData getFreeBetForChannelRequestData();

  void setFreeBetForChannelRequestData(FreeBetForChannelRequestData request);

  void removeSelectionByOutcomeId(String outcomeId);

  void addComplexSelections(ComplexSelection selection);

  void addSelection(String outcomeId);

  void removeComplexSelection(ComplexSelection selection);

  void setBetBuildResponse(BetBuildResponseModel body);

  void setSelectedOutcomeIds(List<String> outcomes);

  boolean isOutcomeIdPresent(String outcomeId);

  void setComplexSelections(List<ComplexSelection> selections);

  void clearAllSelections();

  void setToken(String token);

  String getToken();

  void addOutcomeEvent(String outcomeId, Event event);

  Option<Event> getOutcomeEvent(String outcomeId);

  void removeOutcomeEvent(String outcomeId);

  void removeOutcomesEvents(List<String> outcomeIds);

  void registerPendingTask(UUID uuid, Future futureTask, List<BetRef> betsToReadInBackground);

  void finishTask(UUID uuid);

  void finishTasks();

  Map<UUID, List<BetRef>> getBetsToReadInBackground();

  void clearAllTasks();
}
