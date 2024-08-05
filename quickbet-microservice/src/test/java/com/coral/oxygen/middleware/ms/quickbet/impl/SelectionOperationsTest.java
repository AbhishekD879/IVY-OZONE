package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.SELECTION_EMPTY_OR_ALREADY_ADDED;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.SELECTION_TO_REMOVE_NOT_PRESENT;
import static com.coral.oxygen.middleware.ms.quickbet.impl.SelectionOperations.EMPTY_JSON_RESPONSE;
import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.OveraskReadBetExecutionService;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.ComplexSelection;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.AddSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.utils.BetBuildUtils;
import com.egalacoral.spark.siteserver.model.Event;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuildResponseModel;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.OutcomeDetails;
import io.vavr.collection.HashMap;
import io.vavr.collection.List;
import io.vavr.collection.Map;
import io.vavr.collection.Set;
import io.vavr.control.Option;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class SelectionOperationsTest {

  private static final String OUTCOME_ID = "111";
  private static final String TOKEN = "token";

  private Session sessionMock = mock(Session.class);

  private LiveServService liveServServiceMock = mock(LiveServService.class);

  private OveraskReadBetExecutionService overaskReadBetExecutionService =
      mock(OveraskReadBetExecutionService.class);
  private SiteServerService siteServerService = mock(SiteServerService.class);
  private BuildBetOperations buildBetOperations = mock(BuildBetOperations.class);

  private SelectionOperations selectionOperations =
      new SelectionOperations(
          buildBetOperations,
          overaskReadBetExecutionService,
          liveServServiceMock,
          siteServerService);

  @Test
  void testRemoveSelectionByOutcomeId() {
    // GIVEN
    String outcomeId = "123";
    when(sessionMock.getSelectedOutcomeIds()).thenReturn(List.of(outcomeId));
    when(sessionMock.isOutcomeIdPresent(outcomeId)).thenReturn(true);
    when(sessionMock.getComplexSelections()).thenReturn(List.empty());
    when(sessionMock.getOutcomeEvent(any())).thenReturn(Option.none());

    when(buildBetOperations.buildBet(any())).thenReturn(getBetBuildResponseModel());

    // WHEN
    selectionOperations.removeSelection(sessionMock, outcomeId);

    // THEN
    verify(sessionMock).removeSelectionByOutcomeId(outcomeId);
    verify(sessionMock).unsubscribeFromOutcomesIdsRooms(List.of(outcomeId));
  }

  @Test
  void testRemoveSelectionSubscribesToRemainingSelections() {
    // GIVEN
    String outcomeId = "123";
    String outcomeId2 = "12";

    BetBuildResponseModel response = getBetBuildResponseModel(Integer.parseInt(outcomeId2), 2, 3);

    when(buildBetOperations.buildBet(any())).thenReturn(response);
    when(sessionMock.isOutcomeIdPresent(outcomeId)).thenReturn(true);

    // WHEN
    selectionOperations.removeSelection(sessionMock, outcomeId);

    // THEN
    ArgumentCaptor<List<String>> unsubscribeCaptor = ArgumentCaptor.forClass(List.class);
    verify(sessionMock).unsubscribeFromOutcomesIdsRooms(unsubscribeCaptor.capture());
    assertThat(unsubscribeCaptor.getValue()).hasSize(1);
    assertThat(unsubscribeCaptor.getValue().get(0)).isEqualTo(outcomeId);

    ArgumentCaptor<Map<String, Set<String>>> subscribeCaptor = ArgumentCaptor.forClass(Map.class);
    verify(sessionMock).subscribeToRooms(subscribeCaptor.capture());
    assertThat(subscribeCaptor.getValue()).hasSize(1);
    assertThat(subscribeCaptor.getValue().containsKey(outcomeId2)).isTrue();
    assertThat(subscribeCaptor.getValue().get(outcomeId2).get()).hasSize(5);
  }

  @Test
  void shouldCallBetBuildAndProcessFurtherRequestWhenSecondCallHasNewOutcomeId() {
    // GIVEN
    when(sessionMock.getOutcomeEvent(any())).thenReturn(Option.none());
    when(sessionMock.getSelectedOutcomeIds()).thenReturn(List.of("1", "2"));
    when(sessionMock.getComplexSelections()).thenReturn(List.empty());
    BetBuildResponseModel betBuildResponseModel = getBetBuildResponseModel();
    when(buildBetOperations.buildBet(any())).thenReturn(betBuildResponseModel);

    AddSelectionRequest firstAddSelectionRequest = new AddSelectionRequest(OUTCOME_ID);
    mockSiteServerInteraction(List.of("1", "2"), List.of("1", "2"), List.of("99", "98"));
    selectionOperations.addSelection(sessionMock, firstAddSelectionRequest);

    String newOutcome = "333";
    AddSelectionRequest secondAddSelectionRequestWithNewOutcome =
        new AddSelectionRequest(newOutcome);

    // WHEN
    selectionOperations.addSelection(sessionMock, secondAddSelectionRequestWithNewOutcome);

    // THEN
    verify(sessionMock).addSelection(eq(newOutcome));
    verify(buildBetOperations, times(2)).buildBet(any());
  }

  @Test
  void restoreStateWhenSelectionsAreEmpty() {
    // GIVEN
    when(sessionMock.getSelectedOutcomeIds()).thenReturn(List.empty());
    when(sessionMock.getComplexSelections()).thenReturn(List.empty());

    // WHEN
    selectionOperations.restoreState(sessionMock, null);

    // THEN
    verify(buildBetOperations, never()).buildBet(sessionMock);
  }

  @Test
  void restoreStateWhenComplexSelectionsAreNotEmpty() {
    // GIVEN
    when(sessionMock.getSelectedOutcomeIds()).thenReturn(List.empty());
    when(sessionMock.getOutcomeEvent(any())).thenReturn(Option.none());
    when(sessionMock.getComplexSelections())
        .thenReturn(
            List.of(
                new ComplexSelection(
                    ComplexSelection.Type.COMBINATION_FORECAST, List.of("1", "2"))));
    BetBuildResponseModel betBuildResponseModel = getBetBuildResponseModel();
    when(buildBetOperations.buildBet(any())).thenReturn(betBuildResponseModel);
    mockSiteServerInteraction(List.of("1", "2"), List.of("1", "2"), List.of("99", "98"));
    // WHEN
    selectionOperations.restoreState(sessionMock, null);

    // THEN
    verify(buildBetOperations, atLeastOnce()).buildBet(sessionMock);
  }

  @Test
  void noScheduleReadBetsWhenBetsToReadInBackgroundEmpty() {
    // GIVEN
    when(sessionMock.getSelectedOutcomeIds()).thenReturn(List.empty());
    when(sessionMock.getComplexSelections()).thenReturn(List.empty());
    when(sessionMock.getBetsToReadInBackground()).thenReturn(HashMap.empty());

    // WHEN
    selectionOperations.restoreState(sessionMock, TOKEN);

    // THEN
    verify(overaskReadBetExecutionService, never()).scheduleReadBet(any(), any(), any());
  }

  @Test
  void scheduleReadBetsWhenBetsToReadInBackgroundNotEmpty() {
    // GIVEN
    when(sessionMock.getSelectedOutcomeIds()).thenReturn(List.empty());
    when(sessionMock.getComplexSelections()).thenReturn(List.empty());
    UUID taskId = UUID.randomUUID();
    BetRef bedRef = new BetRef();
    bedRef.setId("1");
    when(sessionMock.getBetsToReadInBackground()).thenReturn(HashMap.of(taskId, List.of(bedRef)));

    // WHEN
    selectionOperations.restoreState(sessionMock, TOKEN);

    // THEN
    verify(overaskReadBetExecutionService).scheduleReadBet(sessionMock, List.of(bedRef), TOKEN);
  }

  @Test
  void shouldNotCallBetBuildAndReturnProperMessageForRequestHavingOutcomesAlreadyAdded() {
    // GIVEN
    when(sessionMock.isOutcomeIdPresent(OUTCOME_ID)).thenReturn(true);
    AddSelectionRequest selectionWithOutcomesAlreadyAdded = new AddSelectionRequest(OUTCOME_ID);

    // WHEN
    selectionOperations.addSelection(sessionMock, selectionWithOutcomesAlreadyAdded);

    // THEN
    verify(sessionMock).sendData(SELECTION_EMPTY_OR_ALREADY_ADDED.code(), EMPTY_JSON_RESPONSE);
  }

  @Test
  void shouldNotCallBppWhenSelectionIsEmpty() {
    // GIVEN
    AddSelectionRequest addSelectionRequest = new AddSelectionRequest(null);

    // WHEN
    selectionOperations.addSelection(sessionMock, addSelectionRequest);

    // THEN
    verify(buildBetOperations, never()).buildBet(any());
  }

  @Test
  void shouldReturnProperResponseCodeAndNotCallBetBuildWhenOutcomeIdIsNonExisting() {
    // GIVEN
    when(sessionMock.isOutcomeIdPresent(OUTCOME_ID)).thenReturn(false);

    // WHEN
    selectionOperations.removeSelection(sessionMock, OUTCOME_ID);

    // THEN
    verify(sessionMock).sendData(SELECTION_TO_REMOVE_NOT_PRESENT.code(), EMPTY_JSON_RESPONSE);
    verify(buildBetOperations, never()).buildBet(any());
  }

  @Test
  void shouldCallBuildBetDuringSelectionRemovalWhenOutcomeIdExist() {
    // GIVEN
    BetBuildResponseModel response = getBetBuildResponseModel();
    when(buildBetOperations.buildBet(any())).thenReturn(response);

    when(sessionMock.getSelectedOutcomeIds()).thenReturn(List.of(OUTCOME_ID));
    when(sessionMock.isOutcomeIdPresent(OUTCOME_ID)).thenReturn(true);
    when(sessionMock.getComplexSelections()).thenReturn(List.empty());
    when(sessionMock.getOutcomeEvent(any())).thenReturn(Option.none());

    // WHEN
    selectionOperations.removeSelection(sessionMock, OUTCOME_ID);

    // THEN
    verify(buildBetOperations).buildBet(any());
  }

  @Test
  void shouldThrowExceptionWhenOutcomeIdIsNotInSiteServ() {
    // given
    AddSelectionRequest addSelectionRequest = new AddSelectionRequest(OUTCOME_ID);
    when(siteServerService.getEventsForOutcomeIds(any())).thenReturn(List.empty());
    when(sessionMock.getSelectedOutcomeIds()).thenReturn(List.of(OUTCOME_ID));
    when(sessionMock.getComplexSelections()).thenReturn(List.empty());
    when(sessionMock.getOutcomeEvent(any())).thenReturn(Option.none());

    // then
    assertThrows(
        SiteServException.class,
        () -> {
          selectionOperations.addSelection(sessionMock, addSelectionRequest);
        });
  }

  @Test
  void test_complexSelections() {
    Session session = mock(Session.class);
    ComplexSelection complexSelection =
        new ComplexSelection(ComplexSelection.Type.COMBINATION_FORECAST, null);
    List<ComplexSelection> complexSelectionList = List.of(complexSelection);
    when(session.getComplexSelections()).thenReturn(complexSelectionList);
    boolean val = selectionOperations.validateAddComplexSelection(session, complexSelection);
    assertEquals(false, val);
  }

  @Test
  void test_remove_complexSelections() {
    Session session = mock(Session.class);
    List<ComplexSelection> complexSelectionList = List.empty();
    ComplexSelection complexSelection =
        new ComplexSelection(ComplexSelection.Type.COMBINATION_FORECAST, null);
    complexSelectionList.append(complexSelection);
    when(session.getComplexSelections()).thenReturn(complexSelectionList);
    ComplexSelection complexSelection1 =
        new ComplexSelection(ComplexSelection.Type.COMBINATION_TRICAST, null);
    boolean val = selectionOperations.validateRemoveComplexSelection(session, complexSelection1);
    assertEquals(false, val);
  }

  private BetBuildResponseModel getBetBuildResponseModel() {
    return getBetBuildResponseModel(1, 2, 3);
  }

  private BetBuildResponseModel getBetBuildResponseModel(int id, int eventId, int marketId) {
    BetBuildResponseModel betBuildResponseModel = new BetBuildResponseModel();
    betBuildResponseModel.getOutcomeDetails().add(outcomeDetailsOf(id, eventId, marketId));
    return betBuildResponseModel;
  }

  private OutcomeDetails outcomeDetailsOf(int id, int eventId, int marketId) {
    OutcomeDetails result = new OutcomeDetails();
    result.setId(String.valueOf(id));
    result.setEventId(String.valueOf(eventId));
    result.setMarketId(String.valueOf(marketId));
    return result;
  }

  private void mockSiteServerInteraction(
      List<String> outcomeIds, List<String> eventIds, List<String> marketIds) {
    List<Event> events =
        BetBuildUtils.outcomeToEventWithEventAndMarketId(outcomeIds, eventIds, marketIds);
    when(siteServerService.getEventsForOutcomeIds(any())).thenReturn(events);
  }
}
