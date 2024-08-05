package com.coral.oxygen.middleware.ms.quickbet.impl;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.ComplexSelection;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.UIPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.AddComplexSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.AddSelectionRequest;
import io.vavr.collection.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class QuickBetServiceV2Test {

  private final Session sessionMock = mock(Session.class);

  @Mock private SelectionOperations selectionOperationsMock;
  @Mock private PlaceBetOperations placeBetOperations;
  @Mock private OnceExecutor onceExecutor;
  @Mock private LuckDipPlaceBetOperationHandler luckDipPlaceBetOperationHandler;

  @InjectMocks private QuickBetServiceV2 quickBetServiceV2;

  @Test
  void addSelectionTest() {
    // GIVEN
    when(sessionMock.getToken()).thenReturn("token");
    AddSelectionRequest addSelectionRequest = new AddSelectionRequest("1234");

    // WHEN
    quickBetServiceV2.addSelection(sessionMock, addSelectionRequest);

    // THEN
    verify(selectionOperationsMock).addSelection(sessionMock, addSelectionRequest);
  }

  @Test
  void removeOneSelectionTest() {
    // GIVEN
    String outcomeId = "1234";
    when(sessionMock.getToken()).thenReturn("token");

    // WHEN
    quickBetServiceV2.removeOneSelection(sessionMock, outcomeId);

    // THEN
    verify(selectionOperationsMock).removeSelection(sessionMock, outcomeId);
  }

  @Test
  void addComplexSelectionTest() {
    // GIVEN
    AddComplexSelectionRequest addComplexSelectionRequest =
        new AddComplexSelectionRequest(List.of("111"), ComplexSelection.Type.SCORECAST);

    // WHEN
    quickBetServiceV2.addComplexSelection(sessionMock, addComplexSelectionRequest);

    // THEN
    verify(selectionOperationsMock).addComplexSelection(sessionMock, addComplexSelectionRequest);
  }

  @Test
  void placeBetTest() {
    // GIVEN
    String bppToken = "token";
    when(sessionMock.getToken()).thenReturn(bppToken);
    UIPlaceBetRequest uiPlaceBetRequest = new UIPlaceBetRequest("", "", "", List.empty());

    // WHEN
    quickBetServiceV2.placeBet(sessionMock, uiPlaceBetRequest);

    // THEN
    verify(onceExecutor).executeOnceDuringTimePeriod(eq(bppToken), any(), any(), any());
  }

  @Test
  void placeBetWithError() {
    // GIVEN
    String bppToken = "notEmptyToken";
    when(sessionMock.getToken()).thenReturn(bppToken);
    UIPlaceBetRequest uiPlaceBetRequest = new UIPlaceBetRequest("", "", "", List.empty());

    Mockito.doAnswer(
            invocation -> {
              ((Runnable) invocation.getArguments()[2]).run();
              return null;
            })
        .when(onceExecutor)
        .executeOnceDuringTimePeriod(eq(bppToken), any(), any(), any());

    // WHEN
    quickBetServiceV2.placeBet(sessionMock, uiPlaceBetRequest);

    // THEN
    verify(onceExecutor).executeOnceDuringTimePeriod(eq(bppToken), any(), any(), any());
  }

  @Test
  void testlogin() {
    quickBetServiceV2.login(sessionMock, "tedftfetdfedtfdt");
    quickBetServiceV2.logout(sessionMock);
    verify(sessionMock, times(2)).sendData(Mockito.any(), Mockito.any());
  }
}
