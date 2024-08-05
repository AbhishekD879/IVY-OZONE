package com.ladbrokescoral.oxygen.betpackmp.scheduler;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.when;

import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetOffer;
import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import com.ladbrokescoral.oxygen.betpackmp.kafka.KafkaBetPacksPublisher;
import com.ladbrokescoral.oxygen.betpackmp.redis.ActiveBetPacks;
import com.ladbrokescoral.oxygen.betpackmp.redis.BetPackRedisService;
import com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack.BetPackLastMessageCache;
import com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack.BetPackMessage;
import com.ladbrokescoral.oxygen.betpackmp.util.DateUtils;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Modifier;
import java.time.Instant;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class BetPackSchedulerTest implements WithAssertions {

  @Mock private BetPackLastMessageCache betPackLastMessageCache;

  @Mock private KafkaBetPacksPublisher kafkaBetPackPublisher;

  @Mock private BetPackRedisService betPackRedisService;

  @Mock private MasterSlaveExecutor masterSlaveExecutor;

  @InjectMocks private BetPackScheduler betPackScheduler;

  @BeforeEach
  void setUp() {
    betPackScheduler =
        new BetPackScheduler(
            betPackLastMessageCache,
            kafkaBetPackPublisher,
            betPackRedisService,
            masterSlaveExecutor);
  }

  @Test
  void scheduleTaskUsingCronExpression_Executed_Test() {
    doAnswer(
            invocation -> {
              Runnable task = (Runnable) invocation.getArguments()[0];
              task.run();
              return null;
            })
        .when(masterSlaveExecutor)
        .executeIfMaster(any(Runnable.class), any(Runnable.class));
    when(betPackRedisService.getActiveBetPacks(anyString()))
        .thenReturn(new ActiveBetPacks(new ArrayList<>()));
    when(betPackLastMessageCache.findAllById(anyList())).thenReturn(createBetPackMessage());
    Assertions.assertDoesNotThrow(() -> betPackScheduler.scheduleTaskUsingCronExpression());
  }

  @Test
  void scheduleTaskUsingCronExpression_EmptyBetPackMessages_Test() {
    doAnswer(
            invocation -> {
              Runnable task = (Runnable) invocation.getArguments()[0];
              task.run();
              return null;
            })
        .when(masterSlaveExecutor)
        .executeIfMaster(any(Runnable.class), any(Runnable.class));
    when(betPackRedisService.getActiveBetPacks(anyString()))
        .thenReturn(new ActiveBetPacks(new ArrayList<>()));
    when(betPackLastMessageCache.findAllById(anyList())).thenReturn(Collections.emptyList());
    Assertions.assertDoesNotThrow(() -> betPackScheduler.scheduleTaskUsingCronExpression());
  }

  @Test
  void scheduleTaskUsingCronExpression_MasterSlaveNotExecuted_Test() {
    doAnswer(
            invocation -> {
              Runnable task = (Runnable) invocation.getArguments()[1];
              task.run();
              return null;
            })
        .when(masterSlaveExecutor)
        .executeIfMaster(any(Runnable.class), any(Runnable.class));
    Assertions.assertDoesNotThrow(() -> betPackScheduler.scheduleTaskUsingCronExpression());
  }

  @Test
  void testConstructorIsPrivate() throws Exception {
    Constructor<DateUtils> constructor = DateUtils.class.getDeclaredConstructor();
    assertTrue(Modifier.isPrivate(constructor.getModifiers()));
    constructor.setAccessible(true);
    assertThrows(InvocationTargetException.class, constructor::newInstance);
  }

  private List<BetPackMessage> createBetPackMessage() {
    List<BetPackMessage> betPackMessages = new ArrayList<>();
    Instant currentTime = Instant.now().minus(1, ChronoUnit.DAYS);
    BetPackMessage betPackMessage = new BetPackMessage();
    betPackMessage.setBetPackId("629475");
    FreebetOffer freeBetOffer = new FreebetOffer();
    freeBetOffer.setEndTime(convertDates(currentTime.toString()));
    freeBetOffer.setFreebetOfferId("3874557");
    betPackMessage.setMessage(freeBetOffer);
    betPackMessages.add(betPackMessage);
    Instant currentTime2 = Instant.now().plusSeconds(10820);
    BetPackMessage betPackMessage2 = new BetPackMessage();
    betPackMessage2.setBetPackId("439884");
    FreebetOffer freeBetOffer2 = new FreebetOffer();
    freeBetOffer2.setEndTime(convertDates(currentTime2.toString()));
    freeBetOffer2.setFreebetOfferId("986598");
    betPackMessage2.setMessage(freeBetOffer2);
    betPackMessages.add(betPackMessage2);
    Instant currentTime3 = Instant.now().plusSeconds(20000);
    BetPackMessage betPackMessage3 = new BetPackMessage();
    betPackMessage3.setBetPackId("8458745");
    FreebetOffer freeBetOffer3 = new FreebetOffer();
    freeBetOffer3.setEndTime(convertDates(currentTime3.toString()));
    freeBetOffer3.setFreebetOfferId("74748");
    betPackMessage3.setMessage(freeBetOffer3);
    betPackMessages.add(betPackMessage3);
    betPackMessages.add(new BetPackMessage("4567", null));
    return betPackMessages;
  }

  public String convertDates(String date) {
    String DATE_FORMAT = "yyyy-MM-dd HH:mm:ss";
    DateTimeFormatter formatter =
        DateTimeFormatter.ofPattern(DATE_FORMAT).withZone(ZoneId.of("Europe/London"));

    Instant instant = Instant.parse(date);
    return formatter.format(instant);
  }
}
