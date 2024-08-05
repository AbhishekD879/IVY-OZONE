package com.coral.oxygen.middleware.ms.quickbet.impl;

import com.coral.bpp.api.model.bet.api.common.YesNo;
import com.coral.bpp.api.model.bet.api.response.*;
import com.coral.oxygen.middleware.ms.quickbet.BaseSession;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.SessionListener;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.LuckyDipBetPlacementRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Optional;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.core.env.Environment;

@ExtendWith(MockitoExtension.class)
public class LuckDipPlaceBetOperationHandlerTest extends BDDMockito {

  @Mock private SiteServerService siteServerService;
  @Mock private LuckDipService luckyDipService;
  @Mock private LuckDipRNGService luckDipRngService;
  @Mock private Environment environment;
  @InjectMocks private LuckDipPlaceBetOperationHandler luckDipPlaceBetOperationHandler;

  private LuckyDipBetPlacementRequest betPlacementRequestDto;
  private Event event;
  private Session session;
  public static final String BRAND = "BMA";
  private static final String SESSION_ID = "gggd-5555dgg-4564";
  private Bet bet;

  @BeforeEach
  public void setUp() {
    betPlacementRequestDto =
        new LuckyDipBetPlacementRequest("S|H|A0000000", "3/1", "119693182", "WIN");
    event = TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent.json", Event.class);
    SessionStorage<SessionDto> sessionStorage = mock(SessionStorage.class);
    session = new BaseSession(SESSION_ID, sessionStorage);
    bet = new Bet();
    bet.setIsConfirmed(YesNo.Y);
  }

  @Test
  void processLuckDipPlaceBetTestHappyPath() {
    betPlacementRequestDto.setCurrency("GBP");
    when(siteServerService.getEventToOutcomeForMarketForLuckyDip(any()))
        .thenReturn(Optional.of(Arrays.asList(event)));
    when(luckyDipService.findFirst(anyList())).thenReturn(event);
    when(environment.getActiveProfiles()).thenReturn(new String[] {"LB_TST0"});

    doNothing().when(luckyDipService).processLuckyDipPlaceBet(any(), any(), any());

    luckDipPlaceBetOperationHandler.processLuckyDipPlaceBet(session, betPlacementRequestDto);
    Assertions.assertNotNull(luckDipPlaceBetOperationHandler);
  }

  @Test
  void processLuckDipPlaceBetTestWhenEventsNotPresent() {
    when(siteServerService.getEventToOutcomeForMarketForLuckyDip(any()))
        .thenReturn(Optional.empty());

    Assertions.assertThrows(
        NullPointerException.class,
        () -> {
          luckDipPlaceBetOperationHandler.processLuckyDipPlaceBet(session, betPlacementRequestDto);
        });
  }

  @Test
  void processLuckDipPlaceBetTestWhenEventPresentButIsNull() {
    when(siteServerService.getEventToOutcomeForMarketForLuckyDip(any()))
        .thenReturn(Optional.of(new ArrayList<>()));
    when(luckyDipService.findFirst(anyList())).thenReturn(null);
    session.setListener(mock(SessionListener.class));
    luckDipPlaceBetOperationHandler.processLuckyDipPlaceBet(session, betPlacementRequestDto);
    Assertions.assertNotNull(luckDipPlaceBetOperationHandler);
  }

  @Test
  void processLuckDipPlaceBetTestWhenMarketIsNull() {
    when(siteServerService.getEventToOutcomeForMarketForLuckyDip(any()))
        .thenReturn(Optional.of(Collections.singletonList(new Event())));
    when(luckyDipService.findFirst(anyList())).thenReturn(new Event());

    Assertions.assertThrows(
        NullPointerException.class,
        () -> {
          luckDipPlaceBetOperationHandler.processLuckyDipPlaceBet(session, betPlacementRequestDto);
        });
  }

  @Test
  void processLuckDipPlaceBetTestWhenMarketDrillDownTagNameNALads() {
    Event event2 =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent2.json", Event.class);
    when(siteServerService.getEventToOutcomeForMarketForLuckyDip(any()))
        .thenReturn(Optional.of(Collections.singletonList(event2)));
    when(luckyDipService.findFirst(anyList())).thenReturn(event2);
    when(environment.getActiveProfiles()).thenReturn(new String[] {"LB_TST0"});
    Assertions.assertThrows(
        NullPointerException.class,
        () -> {
          luckDipPlaceBetOperationHandler.processLuckyDipPlaceBet(session, betPlacementRequestDto);
        });
  }

  @Test
  void processLuckDipPlaceBetTestWhenMarketDrillDownTagNameNACoral() {
    Event event2 =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent2.json", Event.class);
    when(siteServerService.getEventToOutcomeForMarketForLuckyDip(any()))
        .thenReturn(Optional.of(Collections.singletonList(event2)));
    when(luckyDipService.findFirst(anyList())).thenReturn(event2);
    when(environment.getActiveProfiles()).thenReturn(new String[] {"CR_TST0"});
    Assertions.assertThrows(
        NullPointerException.class,
        () -> {
          luckDipPlaceBetOperationHandler.processLuckyDipPlaceBet(session, betPlacementRequestDto);
        });
  }

  @Test
  void processLuckDipPlaceBetTestWhenMarketDrillDownTagNameNotCorrectLads() {
    Event event3 =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent3.json", Event.class);
    when(siteServerService.getEventToOutcomeForMarketForLuckyDip(any()))
        .thenReturn(Optional.of(Collections.singletonList(event3)));
    when(luckyDipService.findFirst(anyList())).thenReturn(event3);
    when(environment.getActiveProfiles()).thenReturn(new String[] {"LB_TST0"});

    Assertions.assertThrows(
        NullPointerException.class,
        () -> {
          luckDipPlaceBetOperationHandler.processLuckyDipPlaceBet(session, betPlacementRequestDto);
        });
  }

  @Test
  void processLuckDipPlaceBetTestWhenMarketDrillDownTagNameNotCorrectCoral() {
    Event event3 =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent3.json", Event.class);
    when(siteServerService.getEventToOutcomeForMarketForLuckyDip(any()))
        .thenReturn(Optional.of(Collections.singletonList(event3)));
    when(luckyDipService.findFirst(anyList())).thenReturn(event3);
    when(environment.getActiveProfiles()).thenReturn(new String[] {"CR_TST0"});

    Assertions.assertThrows(
        NullPointerException.class,
        () -> {
          luckDipPlaceBetOperationHandler.processLuckyDipPlaceBet(session, betPlacementRequestDto);
        });
  }

  @Test
  void processLuckDipPlaceBetTestWhenEventSortCodeNA() {
    Event event4 =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent4.json", Event.class);
    when(siteServerService.getEventToOutcomeForMarketForLuckyDip(any()))
        .thenReturn(Optional.of(Collections.singletonList(event4)));
    when(luckyDipService.findFirst(anyList())).thenReturn(event4);
    when(environment.getActiveProfiles()).thenReturn(new String[] {"CR_TST0"});
    Assertions.assertThrows(
        NullPointerException.class,
        () -> {
          luckDipPlaceBetOperationHandler.processLuckyDipPlaceBet(session, betPlacementRequestDto);
        });
  }

  @Test
  void processLuckDipPlaceBetTestWhenEventSortCodeNotCorrect() {
    Event event5 =
        TestUtils.deserializeWithJackson("impl/LuckyDipService/testEvent5.json", Event.class);
    when(siteServerService.getEventToOutcomeForMarketForLuckyDip(any()))
        .thenReturn(Optional.of(Collections.singletonList(event5)));
    when(luckyDipService.findFirst(anyList())).thenReturn(event5);

    when(environment.getActiveProfiles()).thenReturn(new String[] {"CR_TST0"});
    Assertions.assertThrows(
        NullPointerException.class,
        () -> {
          luckDipPlaceBetOperationHandler.processLuckyDipPlaceBet(session, betPlacementRequestDto);
        });
  }

  @Test
  void processLuckDipPlaceBetTestWhenOutcomeNotActive() {
    Event testEventWithOutcomeNotActive =
        TestUtils.deserializeWithJackson(
            "impl/LuckyDipService/testEventWhenOutcomeNotActiveAndNotDisplayed.json", Event.class);
    when(siteServerService.getEventToOutcomeForMarketForLuckyDip(any()))
        .thenReturn(Optional.of(Collections.singletonList(testEventWithOutcomeNotActive)));
    when(luckyDipService.findFirst(anyList())).thenReturn(testEventWithOutcomeNotActive);
    when(environment.getActiveProfiles()).thenReturn(new String[] {"CR_TST0"});

    Assertions.assertThrows(
        NullPointerException.class,
        () -> {
          luckDipPlaceBetOperationHandler.processLuckyDipPlaceBet(session, betPlacementRequestDto);
        });
  }

  @Test
  void processLuckDipPlaceBetTestWhenOutcomeIsNull() {
    Event testEventWithOutcomeNA =
        TestUtils.deserializeWithJackson(
            "impl/LuckyDipService/testEventWhenOutcomeActiveNAAndDisplayed.json", Event.class);
    when(siteServerService.getEventToOutcomeForMarketForLuckyDip(any()))
        .thenReturn(Optional.of(Collections.singletonList(testEventWithOutcomeNA)));
    when(luckyDipService.findFirst(anyList())).thenReturn(testEventWithOutcomeNA);
    when(environment.getActiveProfiles()).thenReturn(new String[] {"CR_TST0"});

    Assertions.assertThrows(
        NullPointerException.class,
        () -> {
          luckDipPlaceBetOperationHandler.processLuckyDipPlaceBet(session, betPlacementRequestDto);
        });
  }

  @Test
  void processLuckDipPlaceBetTestWhenMarketIsSuspended() {
    Event testEventWithOutcomeNA =
        TestUtils.deserializeWithJackson(
            "impl/LuckyDipService/testEventWhenMarketNotActive.json", Event.class);
    when(siteServerService.getEventToOutcomeForMarketForLuckyDip(any()))
        .thenReturn(Optional.of(Collections.singletonList(testEventWithOutcomeNA)));
    when(luckyDipService.findFirst(anyList())).thenReturn(testEventWithOutcomeNA);

    Assertions.assertThrows(
        NullPointerException.class,
        () -> {
          luckDipPlaceBetOperationHandler.processLuckyDipPlaceBet(session, betPlacementRequestDto);
        });
  }
}
