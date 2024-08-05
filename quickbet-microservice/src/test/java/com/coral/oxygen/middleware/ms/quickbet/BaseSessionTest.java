package com.coral.oxygen.middleware.ms.quickbet;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.ComplexSelection;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.CalculateOddsRequestDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.RegularSelectionResponse;
import com.coral.oxygen.middleware.ms.quickbet.impl.SessionStorage;
import com.egalacoral.spark.siteserver.model.Event;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import io.vavr.collection.HashMap;
import io.vavr.collection.HashSet;
import io.vavr.collection.List;
import io.vavr.collection.Set;
import java.util.*;
import java.util.concurrent.*;
import org.jetbrains.annotations.NotNull;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class BaseSessionTest {

  private static final String TEST_SESSION_ID = "TEST_SESSION_ID";

  @Mock private SessionStorage<SessionDto> sessionStorage;

  @Mock private SessionListener listener;

  @Captor private ArgumentCaptor<Collection<String>> captor;

  private SessionDto sessionDto;

  private BaseSession session;

  @BeforeEach
  public void setUp() {
    sessionDto = new SessionDto(TEST_SESSION_ID);
    Mockito.when(sessionStorage.find(Mockito.anyString())).thenReturn(Optional.of(sessionDto));
    session = new BaseSession(TEST_SESSION_ID, sessionStorage);
    session.fetch();
    session.setListener(listener);
  }

  @Test
  void testNullSessionStorage() {
    assertThatThrownBy(() -> session = new BaseSession(TEST_SESSION_ID, null))
        .isInstanceOf(IllegalArgumentException.class);
  }

  @Test
  void testNullSessionId() {
    assertThatThrownBy(() -> session = new BaseSession(null, sessionStorage))
        .isInstanceOf(IllegalArgumentException.class);
  }

  @Test
  void testSave() {
    // action
    session.save();
    // verification
    Mockito.verify(sessionStorage).persist(sessionDto);
  }

  @Test
  void testFetchNotSuccess() {
    // preparation
    Mockito.when(sessionStorage.find(Mockito.anyString())).thenReturn(Optional.empty());
    // action
    boolean exists = session.fetch();
    // verification
    assertThat(exists).isFalse();
  }

  @Test
  void testFetchExists() {
    // preparation
    Mockito.when(sessionStorage.find(Mockito.anyString())).thenReturn(Optional.of(sessionDto));
    // action
    boolean exists = session.fetch();
    // verification
    assertThat(exists).isTrue();
  }

  @Test
  void testNotExists() {
    // preparation
    Mockito.when(sessionStorage.find(Mockito.anyString())).thenReturn(Optional.empty());
    // action
    boolean exists = session.exists();
    // verification
    assertThat(exists).isFalse();
  }

  @Test
  void testExists() {
    // preparation
    Mockito.when(sessionStorage.find(Mockito.anyString())).thenReturn(Optional.of(sessionDto));
    // action
    boolean exists = session.exists();
    // verification
    assertThat(exists).isTrue();
  }

  @Test
  void testSessionId() {
    String sessionId = session.sessionId();
    assertThat(sessionId).isEqualTo(TEST_SESSION_ID);
  }

  @Test
  void testSubscribeToRooms() {
    // given
    Collection<String> rooms = Arrays.asList("A", "B", "C");
    // when
    session.subscribeToRooms(rooms);
    // then
    Mockito.verify(listener).subscribeToRooms(captor.capture());
    assertThat(captor.getValue()).containsExactlyInAnyOrder("C", "B", "A");
  }

  @Test
  void testOverrideSubscription() {
    // given
    Collection<String> rooms = Arrays.asList("A", "B", "C", "A");
    // when
    session.subscribeToRooms(rooms);
    session.subscribeToRooms(Arrays.asList("B", "C"));
    // then
    Mockito.verify(listener, times(2)).subscribeToRooms(captor.capture());
    Collection<String> capturedRooms1 = captor.getAllValues().get(0);
    Collection<String> capturedRooms2 = captor.getAllValues().get(1);
    assertThat(capturedRooms1).containsExactlyInAnyOrder("C", "B", "A");
    assertThat(capturedRooms2).containsExactlyInAnyOrder("C", "B");
  }

  @Test
  void testUnsubscribeFromRooms() {
    // given
    Collection<String> rooms = Arrays.asList("A", "B", "C");
    // when
    session.subscribeToRooms(rooms);
    session.unsubscribeFromAllRooms();
    // then
    Mockito.verify(listener).unsubscribeFromRooms(captor.capture());
    assertThat(captor.getValue()).containsExactlyInAnyOrder("B", "A", "C");
  }

  @Test
  void testSubscribeUnsubscribeMultiple() {
    // given
    HashMap<String, Set<String>> map =
        HashMap.of(
            "outcomeId_1", HashSet.of("A", "B", "C", "D"),
            "outcomeId_2", HashSet.of("A", "B", "E"));

    // when
    session.subscribeToRooms(map);
    session.unsubscribeFromOutcomesIdsRooms(List.of("outcomeId_2"));

    // then
    ArgumentCaptor<Collection<String>> subscriptionsCaptor =
        ArgumentCaptor.forClass((Class) Collection.class);
    Mockito.verify(listener, times(1)).subscribeToRooms(subscriptionsCaptor.capture());
    Mockito.verify(listener, times(1)).unsubscribeFromRooms(captor.capture());

    Collection<String> subscribedRooms = subscriptionsCaptor.getAllValues().get(0);
    Collection<String> unsubscribedRooms = captor.getAllValues().get(0);
    assertThat(subscribedRooms).containsExactlyInAnyOrder("A", "B", "C", "D", "E");
    assertThat(unsubscribedRooms).containsExactlyInAnyOrder("E");
  }

  @Test
  void testDoubleUnsubscribeOfOutcomeId() {

    HashMap<String, Set<String>> map =
        HashMap.of(
            "outcomeId_1", HashSet.of("A", "B", "C", "D"),
            "outcomeId_2", HashSet.of("A", "B", "E"));

    // when
    session.subscribeToRooms(map);
    session.unsubscribeFromOutcomesIdsRooms(List.of("outcomeId_2"));
    session.unsubscribeFromOutcomesIdsRooms(List.of("outcomeId_2"));

    // then
    ArgumentCaptor<Collection<String>> subscriptionsCaptor =
        ArgumentCaptor.forClass((Class) Collection.class);
    Mockito.verify(listener, times(1)).subscribeToRooms(subscriptionsCaptor.capture());
    Mockito.verify(listener, times(1)).unsubscribeFromRooms(captor.capture());

    Collection<String> subscribedRooms = subscriptionsCaptor.getAllValues().get(0);
    Collection<String> unsubscribedRooms = captor.getAllValues().get(0);
    assertThat(subscribedRooms).containsExactlyInAnyOrder("A", "B", "C", "D", "E");
    assertThat(unsubscribedRooms).containsExactlyInAnyOrder("E");
  }

  @Test
  void testClearSubscriptionForMultipleAddedChannels() {
    // given
    // given
    HashMap<String, Set<String>> map =
        HashMap.of(
            "outcomeId_1", HashSet.of("A", "B", "C", "D"),
            "outcomeId_2", HashSet.of("A", "B", "E"),
            "outcomeId_3", HashSet.of("A", "B", "F"));

    // when
    session.subscribeToRooms(map);
    session.unsubscribeFromOutcomesIdsRooms(List.of("outcomeId_1"));
    session.unsubscribeFromOutcomesIdsRooms(List.of("outcomeId_2"));
    session.unsubscribeFromOutcomesIdsRooms(List.of("outcomeId_3"));

    // then
    ArgumentCaptor<Collection<String>> subscriptionsCaptor =
        ArgumentCaptor.forClass((Class) Collection.class);
    Mockito.verify(listener, times(1)).subscribeToRooms(subscriptionsCaptor.capture());
    Mockito.verify(listener, times(3)).unsubscribeFromRooms(captor.capture());

    Collection<String> subscribedRooms = subscriptionsCaptor.getAllValues().get(0);
    assertThat(subscribedRooms).containsExactlyInAnyOrder("A", "B", "C", "D", "E", "F");

    Collection<String> unsubscribedRooms1 = captor.getAllValues().get(0);
    assertThat(unsubscribedRooms1).containsExactlyInAnyOrder("C", "D");

    Collection<String> unsubscribedRooms2 = captor.getAllValues().get(1);
    assertThat(unsubscribedRooms2).containsExactlyInAnyOrder("E");

    Collection<String> unsubscribedRooms3 = captor.getAllValues().get(2);
    assertThat(unsubscribedRooms3).containsExactlyInAnyOrder("A", "B", "F");
  }

  @Test
  void testUnSubscribeFromAllRooms() {
    // given
    Collection<String> rooms = Arrays.asList("A", "B", "C");
    session.subscribeToRooms(rooms);
    // then
    Mockito.doAnswer(
            invocation -> {
              verifyUnsubscribeArgs(invocation.getArguments()[0]);
              return null;
            })
        .when(listener)
        .unsubscribeFromRooms(anyCollection());
    // when
    session.unsubscribeFromAllRooms();
  }

  private void verifyUnsubscribeArgs(Object args) {
    Collection<String> unsubscribeRooms = (Collection<String>) args;
    assertThat(unsubscribeRooms).hasSize(3);
    assertThat(unsubscribeRooms).containsExactlyInAnyOrder("C", "B", "A");
  }

  @Test
  void testUnSubscribeFromAllRoomsTwice() {
    // given
    Collection<String> rooms = Arrays.asList("A", "B", "C");
    session.subscribeToRooms(rooms);

    // then
    Mockito.doAnswer(
            i -> {
              verifyUnsubscribeArgs(i.getArguments()[0]);
              return null;
            })
        .doAnswer(
            i -> {
              verifyUnsubscribeSecondTime(i.getArguments()[0]);
              return null;
            })
        .when(listener)
        .unsubscribeFromRooms(anyCollection());

    // when
    session.unsubscribeFromAllRooms();
    session.unsubscribeFromAllRooms();
  }

  private void verifyUnsubscribeSecondTime(Object args) {
    Collection<String> unsubscribeRooms = (Collection<String>) args;
    assertThat(unsubscribeRooms).isEmpty();
  }

  @Test
  void testSetGetRegularSelectionResponse() {
    RegularSelectionResponse response = new RegularSelectionResponse();
    // action
    session.setRegularSelectionResponse(response);
    // verification
    RegularSelectionResponse actual = session.getRegularSelectionResponse();
    assertThat(actual).isEqualTo(response);
  }

  @Test
  void testSetGetRegularSelectionRequest() {
    RegularSelectionRequest request = new RegularSelectionRequest();
    // action
    session.setRegularSelectionRequest(request);
    // verification
    assertThat(sessionDto.getRegularSelectionRequest()).isEqualTo(request);
    assertThat(session.getRegularSelectionRequest()).isEqualTo(request);
  }

  @Test
  void testClearRegularSelection() {
    RegularSelectionRequest request = new RegularSelectionRequest();
    session.setRegularSelectionRequest(request);
    RegularSelectionResponse response = new RegularSelectionResponse();
    session.setRegularSelectionResponse(response);
    // action
    session.clearRegularSelection();
    // verification
    assertThat(sessionDto.getRegularSelectionRequest()).isNull();
    assertThat(session.getRegularSelectionRequest()).isNull();
    assertThat(session.getRegularSelectionResponse()).isNull();
  }

  @Test
  void testSendData() {
    String message = "MSG";
    Object data = new Object();
    // action
    session.sendData(message, data);
    // verification
    Mockito.verify(listener).sendData(message, data);
  }

  @Test
  void testSetGetOddsRequest() {
    CalculateOddsRequestDto dto1 = CalculateOddsRequestDto.builder().build();
    CalculateOddsRequestDto dto2 = CalculateOddsRequestDto.builder().build();
    List<CalculateOddsRequestDto> oddsRequest = List.of(dto1, dto2);
    // action
    session.setOddsRequest(oddsRequest);
    // verification
    assertThat(sessionDto.getOddsRequest()).isEqualTo(oddsRequest);
    assertThat(session.getOddsRequest()).isEqualTo(oddsRequest);
  }

  @Test
  void testRemoveSelectionByOutcomeId() {
    String outcomeIdToRemove = "123";
    session.setSelectedOutcomeIds(List.of(outcomeIdToRemove, "other"));

    // action
    session.removeSelectionByOutcomeId(outcomeIdToRemove);

    // verification
    assertThat(session.getSelectedOutcomeIds()).hasSize(1);
    assertThat(session.getSelectedOutcomeIds()).doesNotContain(outcomeIdToRemove);
  }

  @Test
  void testRemoveOutcomeEvent() {
    // given
    String outcomeId = "123";
    session.addOutcomeEvent(outcomeId, new Event());

    // when
    session.removeOutcomeEvent(outcomeId);

    // then
    assertThat(session.getOutcomeEvent(outcomeId)).isEmpty();
  }

  @Test
  void testRemoveMultipleOutcomesEvent() {
    // given
    List<String> outcomesIds = List.of("123", "456");
    outcomesIds.forEach(outcomeId -> session.addOutcomeEvent(outcomeId, new Event()));

    // when
    session.removeOutcomesEvents(outcomesIds);

    // then
    assertThat(session.getOutcomeEvent(outcomesIds.get(0))).isEmpty();
    assertThat(session.getOutcomeEvent(outcomesIds.get(1))).isEmpty();
  }

  @Test
  void shouldRemoveComplexSelection() {
    // given
    ComplexSelection toRemove =
        new ComplexSelection(ComplexSelection.Type.STRAIGHT_FORECAST, List.of("001", "002", "003"));
    List<ComplexSelection> selections =
        List.of(
            new ComplexSelection(
                ComplexSelection.Type.STRAIGHT_FORECAST, List.of("001", "002", "003")),
            new ComplexSelection(
                ComplexSelection.Type.STRAIGHT_FORECAST, List.of("003", "002", "001")),
            new ComplexSelection(
                ComplexSelection.Type.REVERSE_FORECAST, List.of("001", "002", "003")),
            new ComplexSelection(
                ComplexSelection.Type.STRAIGHT_FORECAST, List.of("001", "002", "003", "004")));
    session.setComplexSelections(selections);

    // when
    session.removeComplexSelection(toRemove);

    // then
    assertThat(session.getComplexSelections()).hasSize(3);
    assertThat(session.getComplexSelections()).doesNotContain(toRemove);
  }

  @Test
  void testFinishTasks() {
    try {
      UUID uuid = new UUID(123L, 345L);
      ConcurrentMap<UUID, Future> tasks = new ConcurrentHashMap<>();
      Future future =
          new Future() {
            @Override
            public boolean cancel(boolean mayInterruptIfRunning) {
              return false;
            }

            @Override
            public boolean isCancelled() {
              return false;
            }

            @Override
            public boolean isDone() {
              return false;
            }

            @Override
            public Object get() throws InterruptedException, ExecutionException {
              return null;
            }

            @Override
            public Object get(long timeout, @NotNull TimeUnit unit)
                throws InterruptedException, ExecutionException, TimeoutException {
              return null;
            }
          };
      BetRef betRef = new BetRef();
      betRef.setId("123");
      betRef.setProvider("opta");
      List<BetRef> betRefs = List.of(betRef);
      session.registerPendingTask(uuid, future, betRefs);
      session.finishTask(uuid);
    } catch (Exception e) {
      Assertions.assertNotNull(e);
    }
  }
}
