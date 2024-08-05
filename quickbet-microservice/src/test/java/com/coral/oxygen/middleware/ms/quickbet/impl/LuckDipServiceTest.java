package com.coral.oxygen.middleware.ms.quickbet.impl;

import com.coral.oxygen.middleware.ms.quickbet.BaseSession;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.SessionListener;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.LuckyDipBetPlacementRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.ReceiptResponseDto;
import com.coral.oxygen.middleware.ms.quickbet.converter.BetToReceiptResponseDtoConverter;
import com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.entain.oxygen.bettingapi.model.bet.api.common.YesNo;
import com.entain.oxygen.bettingapi.model.bet.api.response.*;
import com.entain.oxygen.bettingapi.service.BettingService;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
public class LuckDipServiceTest extends BDDMockito {

  @Mock private BettingService bettingService;

  @Mock private BetToReceiptResponseDtoConverter betToReceiptResponseDtoConverter;
  @Mock private SelectionOperations selectionOperations;
  @InjectMocks private LuckDipService luckDipService;

  private LuckyDipBetPlacementRequest betPlacementRequestDto;
  private Event event;
  private Session session;
  public static final String BRAND = "BMA";
  private static final String SESSION_ID = "gggd-5555dgg-4564";
  private Bet bet;
  private Outcome outcome;

  @BeforeEach
  public void setUp() {
    betPlacementRequestDto =
        new LuckyDipBetPlacementRequest("S|H|A0000000", "3/1", "119693182", "WIN");
    event = TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent.json", Event.class);
    SessionStorage<SessionDto> sessionStorage = mock(SessionStorage.class);
    session = new BaseSession(SESSION_ID, sessionStorage);
    session.setListener(mock(SessionListener.class));
    bet = new Bet();
    bet.setIsConfirmed(YesNo.Y);
    outcome = event.getMarkets().get(0).getOutcomes().get(0);

    betPlacementRequestDto.setCurrency("GBP");
  }

  @Test
  void processLuckyDipPlaceBetTestHappyPath() {
    BetsResponse betsResponse = new BetsResponse();
    betsResponse.setBet(Arrays.asList(bet));
    when(bettingService.placeBet(any(), any()))
        .thenReturn(new GeneralResponse<>(betsResponse, null));
    when(betToReceiptResponseDtoConverter.convert(anyList()))
        .thenReturn(Collections.singletonList(new ReceiptResponseDto()));
    luckDipService.processLuckyDipPlaceBet(
        session, getOutcomesFromEvent(event), betPlacementRequestDto);
    Assertions.assertNotNull(luckDipService);
  }

  @Test
  void processLuckyDipPlaceBetTestWhenPriceNumNull() {
    Event event2 =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent2.json", Event.class);
    luckDipService.processLuckyDipPlaceBet(
        session, getOutcomesFromEvent(event2), betPlacementRequestDto);
    Assertions.assertNotNull(luckDipService);
  }

  @Test
  void processLuckyDipPlaceBetTestWhenPriceDenNull() {
    Event event3 =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent3.json", Event.class);
    luckDipService.processLuckyDipPlaceBet(
        session, getOutcomesFromEvent(event3), betPlacementRequestDto);
    Assertions.assertNotNull(luckDipService);
  }

  @Test
  void processLuckDipPlaceBetTestWhenErrorBodyNotNull() {
    BetsResponse betsResponse = new BetsResponse();
    betsResponse.setBet(Arrays.asList(bet));
    when(bettingService.placeBet(any(), any()))
        .thenReturn(new GeneralResponse<>(betsResponse, new ErrorBody()));
    luckDipService.processLuckyDipPlaceBet(
        session, getOutcomesFromEvent(event), betPlacementRequestDto);
    Assertions.assertNotNull(luckDipService);
  }

  @Test
  void processLuckDipPlaceBetTestWhenErrorBodyNotEmpty() {
    BetsResponse betsResponse = new BetsResponse();
    betsResponse.setBet(Arrays.asList(bet));
    BetError betError = new BetError();
    betError.setCode("404");
    betsResponse.setBetError(Arrays.asList(betError));
    when(bettingService.placeBet(any(), any()))
        .thenReturn(new GeneralResponse<>(betsResponse, null));
    luckDipService.processLuckyDipPlaceBet(
        session, getOutcomesFromEvent(event), betPlacementRequestDto);
    Assertions.assertNotNull(luckDipService);
  }

  @Test
  void processLuckDipPlaceBetTestWhenErrorBodyEmpty() {
    BetsResponse betsResponse = new BetsResponse();
    betsResponse.setBet(Arrays.asList(bet));
    betsResponse.setBetError(new ArrayList<>());
    when(bettingService.placeBet(any(), any()))
        .thenReturn(new GeneralResponse<>(betsResponse, null));
    luckDipService.processLuckyDipPlaceBet(
        session, getOutcomesFromEvent(event), betPlacementRequestDto);
    Assertions.assertNotNull(luckDipService);
  }

  @Test
  void processLuckDipPlaceBetTestWhenBetIsNotConfirmed() {
    BetsResponse betsResponse = new BetsResponse();
    bet.setIsConfirmed(YesNo.N);
    betsResponse.setBet(Arrays.asList(bet));
    when(bettingService.placeBet(any(), any()))
        .thenReturn(new GeneralResponse<>(betsResponse, null));
    luckDipService.processLuckyDipPlaceBet(
        session, getOutcomesFromEvent(event), betPlacementRequestDto);
    Assertions.assertNotNull(luckDipService);
  }

  @Test
  void processLuckDipPlaceBetTestWhenPriceIsNull() {
    Event event6 =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent6.json", Event.class);
    Outcome outcome6 = event6.getMarkets().get(0).getOutcomes().get(0);

    Assertions.assertThrows(
        SiteServException.class,
        () -> {
          luckDipService.processLuckyDipPlaceBet(session, outcome6, betPlacementRequestDto);
        });
  }

  @Test
  void testValidateBppRequestWithWinTypeBlank() {
    betPlacementRequestDto.setWinType("");

    Assertions.assertThrows(
        IllegalArgumentException.class,
        () -> {
          luckDipService.processLuckyDipPlaceBet(session, outcome, betPlacementRequestDto);
        });
  }

  @Test
  void testValidateBppRequestWithStakeBlank() {
    betPlacementRequestDto.setStake("");

    Assertions.assertThrows(
        IllegalArgumentException.class,
        () -> {
          luckDipService.processLuckyDipPlaceBet(session, outcome, betPlacementRequestDto);
        });
  }

  @Test
  void testValidateBppRequestWithMarketIdBlank() {
    betPlacementRequestDto.setMarketId("");

    Assertions.assertThrows(
        IllegalArgumentException.class,
        () -> {
          luckDipService.processLuckyDipPlaceBet(session, outcome, betPlacementRequestDto);
        });
  }

  @Test
  void testValidateBppRequestWithTokenBlank() {
    betPlacementRequestDto.setToken("");

    Assertions.assertThrows(
        IllegalArgumentException.class,
        () -> {
          luckDipService.processLuckyDipPlaceBet(session, outcome, betPlacementRequestDto);
        });
  }

  @Test
  void replaceClientUserAgentTestWithAndroidChannel() throws Exception {
    Method method =
        LuckDipService.class.getDeclaredMethod(
            "replaceClientUserAgent", LuckyDipBetPlacementRequest.class);
    method.setAccessible(true);
    betPlacementRequestDto.setChannel("A");
    method.invoke(luckDipService, betPlacementRequestDto);
    Assertions.assertNotNull(betPlacementRequestDto);
  }

  @Test
  void replaceClientUserAgentTestWithIOSChannel() throws Exception {
    Method method =
        LuckDipService.class.getDeclaredMethod(
            "replaceClientUserAgent", LuckyDipBetPlacementRequest.class);
    method.setAccessible(true);
    betPlacementRequestDto.setChannel("I");
    method.invoke(luckDipService, betPlacementRequestDto);
    Assertions.assertNotNull(betPlacementRequestDto);
  }

  @Test
  void replaceClientUserAgentTestWithDefaultChannel() throws Exception {
    Method method =
        LuckDipService.class.getDeclaredMethod(
            "replaceClientUserAgent", LuckyDipBetPlacementRequest.class);
    method.setAccessible(true);
    betPlacementRequestDto.setChannel("n");

    Assertions.assertThrows(
        InvocationTargetException.class,
        () -> {
          method.invoke(luckDipService, betPlacementRequestDto);
        });
  }

  private Outcome getOutcomesFromEvent(Event event) {
    return event.getMarkets().get(0).getOutcomes().get(0);
  }
}
