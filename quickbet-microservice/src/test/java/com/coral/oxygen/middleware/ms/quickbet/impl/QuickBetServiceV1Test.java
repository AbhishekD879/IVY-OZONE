package com.coral.oxygen.middleware.ms.quickbet.impl;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.LuckyDipBetPlacementRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.RegularPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachPlaceBetRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachSelectionRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.FreeBetForChannelRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

class QuickBetServiceV1Test {

  private SelectionOperations selectionOperations = mock(SelectionOperations.class);
  private BanachBetsOperations banachBetsOperations = mock(BanachBetsOperations.class);
  private FreeBetForChannelOperations freeBetForChannelOperations =
      mock(FreeBetForChannelOperations.class);
  private RegularPlaceBetOperationHandler regularPlaceBetOperationHandler =
      mock(RegularPlaceBetOperationHandler.class);
  private RegularSelectionOperationHandler regularSelectionOperationHandler =
      mock(RegularSelectionOperationHandler.class);
  private LuckDipPlaceBetOperationHandler luckDipPlaceBetOperationHandler =
      mock(LuckDipPlaceBetOperationHandler.class);
  private OnceExecutor onceExecutor = mock(OnceExecutor.class);

  private QuickBetServiceV1 quickBetServiceV1 =
      new QuickBetServiceV1(
          selectionOperations,
          banachBetsOperations,
          freeBetForChannelOperations,
          onceExecutor,
          regularPlaceBetOperationHandler,
          regularSelectionOperationHandler,
          luckDipPlaceBetOperationHandler);

  @Test
  @DisplayName("should place banach bet")
  void banachPlaceBet() {
    // given
    Session session = mock(Session.class);
    BanachPlaceBetRequestData request = new BanachPlaceBetRequestData();
    Mockito.doAnswer(
            invocation -> {
              ((Runnable) invocation.getArguments()[1]).run();
              return null;
            })
        .when(onceExecutor)
        .executeOnceDuringTimePeriod(any(), any(), any(), any());
    // when
    quickBetServiceV1.placeBanachBet(session, request);

    // then
    verify(banachBetsOperations).placeBet(session, request);
  }

  @Test
  void banachPlaceBetWithError() {
    // given
    String bppToken = "notEmptyToken";
    BanachPlaceBetRequestData request = new BanachPlaceBetRequestData();
    request.setToken(bppToken);

    Session sessionMock = mock(Session.class);
    when(sessionMock.getToken()).thenReturn(bppToken);
    Mockito.doAnswer(
            invocation -> {
              ((Runnable) invocation.getArguments()[2]).run();
              return null;
            })
        .when(onceExecutor)
        .executeOnceDuringTimePeriod(eq(bppToken), any(), any(), any());

    // when
    quickBetServiceV1.placeBanachBet(sessionMock, request);

    // then
    verify(onceExecutor).executeOnceDuringTimePeriod(eq(bppToken), any(), any(), any());
  }

  @Test
  @DisplayName("should place regular bet")
  void regularPlaceBet() {
    // given
    Session session = mock(Session.class);
    RegularPlaceBetRequest request = new RegularPlaceBetRequest();
    Mockito.doAnswer(
            invocation -> {
              ((Runnable) invocation.getArguments()[1]).run();
              return null;
            })
        .when(onceExecutor)
        .executeOnceDuringTimePeriod(any(), any(), any(), any());
    // when
    quickBetServiceV1.placeRegularBet(session, request);

    // then
    verify(regularPlaceBetOperationHandler).placeBet(session, request);
  }

  @Test
  void regularPlaceBetWithError() {
    // given
    String bppToken = "notEmptyToken";
    RegularPlaceBetRequest request = new RegularPlaceBetRequest();
    request.setToken(bppToken);

    Session sessionMock = mock(Session.class);
    when(sessionMock.getToken()).thenReturn(bppToken);
    Mockito.doAnswer(
            invocation -> {
              ((Runnable) invocation.getArguments()[2]).run();
              return null;
            })
        .when(onceExecutor)
        .executeOnceDuringTimePeriod(eq(bppToken), any(), any(), any());

    // when
    quickBetServiceV1.placeRegularBet(sessionMock, request);

    // then
    verify(onceExecutor).executeOnceDuringTimePeriod(eq(bppToken), any(), any(), any());
  }

  @Test()
  void testAddRegularSelection() {
    try {
      Session session = mock(Session.class);
      BanachPlaceBetRequestData banachPlaceBetRequestData = new BanachPlaceBetRequestData();
      banachPlaceBetRequestData.setToken("wgdgdvgdvgcvdgcvc");
      quickBetServiceV1.addRegularSelection(session, new RegularSelectionRequest());
      quickBetServiceV1.addBanachSelection(session, new BanachSelectionRequestData());
      quickBetServiceV1.placeBanachBet(session, banachPlaceBetRequestData);
      quickBetServiceV1.placeBanachBet(session, new BanachPlaceBetRequestData());
    } catch (Exception e) {
      Assertions.assertNotNull(e);
    }
  }

  @Test
  @DisplayName("should add freebet token")
  void freebetToken() {
    // given
    Session session = mock(Session.class);
    FreeBetForChannelRequestData request = mock(FreeBetForChannelRequestData.class);

    Mockito.doAnswer(
            invocation -> {
              ((Runnable) invocation.getArguments()[1]).run();
              return null;
            })
        .when(onceExecutor)
        .executeOnceDuringTimePeriod(any(), any(), any(), any());

    // when
    quickBetServiceV1.addFreeBetTokensForChannel(session, request);

    // then
    verify(freeBetForChannelOperations).requestFreeBetTokensForChannel(session, request);
  }

  @Test
  void placeLuckyDipBet() {
    // given
    LuckyDipBetPlacementRequest luckyDipBetPlacementRequest =
        new LuckyDipBetPlacementRequest("S", "3/1", "119693182", "WIN");

    Session sessionMock = mock(Session.class);
    Mockito.doAnswer(
            invocation -> {
              ((Runnable) invocation.getArguments()[1]).run();
              return null;
            })
        .when(onceExecutor)
        .executeOnceDuringTimePeriod(any(), any(), any(), any());

    // when
    quickBetServiceV1.placeLuckyDipBet(sessionMock, luckyDipBetPlacementRequest);

    // then
    verify(luckDipPlaceBetOperationHandler)
        .processLuckyDipPlaceBet(sessionMock, luckyDipBetPlacementRequest);
  }

  @Test
  void luckyDipPlaceBetWithError() {
    // given
    String bppToken = "notEmptyToken";
    LuckyDipBetPlacementRequest luckyDipBetPlacementRequest =
        new LuckyDipBetPlacementRequest(bppToken, "3/1", "119693182", "WIN");

    Session sessionMock = mock(Session.class);
    when(sessionMock.getToken()).thenReturn(bppToken);
    Mockito.doAnswer(
            invocation -> {
              ((Runnable) invocation.getArguments()[2]).run();
              return null;
            })
        .when(onceExecutor)
        .executeOnceDuringTimePeriod(eq(bppToken), any(), any(), any());

    // when
    quickBetServiceV1.placeLuckyDipBet(sessionMock, luckyDipBetPlacementRequest);

    // then
    verify(onceExecutor).executeOnceDuringTimePeriod(eq(bppToken), any(), any(), any());
  }
}
