package com.ladbrokescoral.oxygen.betpackmp.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetOffer;
import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import com.ladbrokescoral.oxygen.betpackmp.redis.ActiveBetPacks;
import com.ladbrokescoral.oxygen.betpackmp.redis.BetPackRedisService;
import com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack.BetPackMessage;
import com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack.BetPackRedisOperations;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Optional;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.util.ReflectionTestUtils;
import reactor.core.publisher.Mono;

@ExtendWith(MockitoExtension.class)
class ActiveBetPacksServiceTest implements WithAssertions {

  @Mock private BetPackRedisService betPackRedisRepoService;
  @Mock private CmsService cmsService;
  @Mock private BetPackService betPackService;
  @Mock private BetPackRedisOperations betPackRedisOperations;
  @Mock private MasterSlaveExecutor masterSlaveExecutor;

  @InjectMocks private ActiveBetPacksService activeBetPacksService;

  @BeforeEach
  void setUp() {
    activeBetPacksService =
        new ActiveBetPacksService(
            betPackRedisRepoService,
            cmsService,
            betPackService,
            betPackRedisOperations,
            masterSlaveExecutor);
    ReflectionTestUtils.setField(activeBetPacksService, "cmsBand", "bma");
  }

  @Test
  void loadActiveBetPacksTest() {
    doAnswer(
            invocation -> {
              Runnable task = (Runnable) invocation.getArguments()[0];
              task.run();
              return null;
            })
        .when(masterSlaveExecutor)
        .executeIfMaster(any(Runnable.class), any(Runnable.class));
    when(cmsService.getActiveBetPackIds(anyString()))
        .thenReturn(Mono.just(Arrays.asList("876", "545")));
    when(betPackRedisRepoService.save(any(ActiveBetPacks.class)))
        .thenReturn(new ActiveBetPacks(new ArrayList<>()));
    when(betPackRedisOperations.getLastSavedMessage(anyString()))
        .thenReturn(Optional.of(new BetPackMessage("packId", new FreebetOffer())));
    Assertions.assertDoesNotThrow(() -> activeBetPacksService.loadActiveBetPacks());
  }

  @Test
  void loadActiveBetPacks_EmptyBetPackIdsTest() {
    doAnswer(
            invocation -> {
              Runnable task = (Runnable) invocation.getArguments()[0];
              task.run();
              return null;
            })
        .when(masterSlaveExecutor)
        .executeIfMaster(any(Runnable.class), any(Runnable.class));
    when(cmsService.getActiveBetPackIds(anyString()))
        .thenReturn(Mono.just(Collections.emptyList()));
    Assertions.assertDoesNotThrow(() -> activeBetPacksService.loadActiveBetPacks());
  }

  @Test
  void loadActiveBetPacks_EmptyLastSavedMessageTest() {
    doAnswer(
            invocation -> {
              Runnable task = (Runnable) invocation.getArguments()[0];
              task.run();
              return null;
            })
        .when(masterSlaveExecutor)
        .executeIfMaster(any(Runnable.class), any(Runnable.class));
    when(cmsService.getActiveBetPackIds(anyString()))
        .thenReturn(Mono.just(Arrays.asList("876", "545")));
    when(betPackRedisRepoService.save(any(ActiveBetPacks.class)))
        .thenReturn(new ActiveBetPacks(new ArrayList<>()));
    when(betPackRedisOperations.getLastSavedMessage(anyString())).thenReturn(Optional.empty());
    Assertions.assertDoesNotThrow(() -> activeBetPacksService.loadActiveBetPacks());
  }

  @Test
  void loadActiveBetPacksFailureTest() {
    doAnswer(
            invocation -> {
              Runnable task = (Runnable) invocation.getArguments()[1];
              task.run();
              return null;
            })
        .when(masterSlaveExecutor)
        .executeIfMaster(any(Runnable.class), any(Runnable.class));
    Assertions.assertDoesNotThrow(() -> activeBetPacksService.loadActiveBetPacks());
  }
}
