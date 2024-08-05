package com.entain.oxygen.betbuilder_middleware.config;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import com.entain.oxygen.betbuilder_middleware.redis.dto.CombinationCache;
import com.entain.oxygen.betbuilder_middleware.repository.RedissonCombinationRepository;
import java.util.*;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mockito;
import org.redisson.api.*;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@ExtendWith(SpringExtension.class)
class RedissonCombinationRepositoryTest {
  @MockBean RLocalCachedMapReactive redissonCombinationEntities;
  @MockBean RedissonReactiveClient redissonReactiveClient;
  @MockBean RedissonProperties redissonProperties;
  RedissonCombinationRepository redissonCombinationRepository;
  RMapReactive rMapReactive;
  RBatchReactive rBatchReactive;
  RSetReactive rSetReactive;

  @BeforeEach
  void setUp() {
    Mockito.when(redissonReactiveClient.getLocalCachedMap(Mockito.anyString(), any()))
        .thenReturn(redissonCombinationEntities);
    redissonCombinationRepository = new RedissonCombinationRepository(redissonReactiveClient);
    rBatchReactive = mock(RBatchReactive.class);
    rMapReactive = mock(RMapReactive.class);
    rSetReactive = mock(RSetReactive.class);
    when(redissonReactiveClient.createBatch()).thenReturn(rBatchReactive);
    when(rBatchReactive.getMap("COMBINATION_MAP")).thenReturn(rMapReactive);
    when(rBatchReactive.getSet(Mockito.any())).thenReturn(rSetReactive);
  }

  @Test
  void testsaveCombinations() {
    Map<String, CombinationCache> combinationCacheMap = new HashMap<>();
    CombinationCache combinationCache = new CombinationCache();
    BatchResult mockBatchResult = mock(BatchResult.class);
    combinationCache.setId("1715163515451");
    combinationCache.setOEId("14918088");
    combinationCache.setHash("374443B4ABF98D75C95A9F374ABAD5CB560523E78B91C3BA069CF465CC6DE424");
    combinationCache.setSportId(16);
    combinationCacheMap.put(
        "374443B4ABF98D75C95A9F374ABAD5CB560523E78B91C3BA069CF465CC6DE424", combinationCache);
    when(rMapReactive.fastPutIfAbsent(Mockito.anyString(), Mockito.any()))
        .thenReturn(Mono.just(true));
    when(rSetReactive.add(Mockito.any())).thenReturn(Mono.just(true));
    Mockito.when(rBatchReactive.execute()).thenReturn(Mono.just(mockBatchResult));
    redissonCombinationRepository.saveCombinations(combinationCacheMap);
    Assertions.assertNotNull(combinationCache);
  }

  @Test
  void testgetCombinationsByOeId() {
    Mockito.when(redissonReactiveClient.getSet(Mockito.anyString())).thenReturn(rSetReactive);
    Mockito.when(rSetReactive.iterator()).thenReturn(Flux.just("abc", "def"));
    Assertions.assertNotNull(redissonCombinationRepository.getCombinationsByOeId("aa"));
  }

  @Test
  void testDeleteCombinations() {
    List<Object> sgpIds = new ArrayList<>();
    sgpIds.add("abc");
    sgpIds.add("def");

    Mockito.when(rSetReactive.delete()).thenReturn(Mono.just(true));
    Mockito.when(rMapReactive.fastRemove(Mockito.any())).thenReturn(Mono.just("1l"));
    Mockito.when(rBatchReactive.execute()).thenReturn(Mono.empty());
    redissonCombinationRepository.deleteCombinations("123", sgpIds);
    Assertions.assertNotNull(sgpIds);
  }

  @Test
  void getCombinationsTest() {
    Mockito.when(redissonCombinationRepository.getCombinations(Mockito.any()))
        .thenReturn(Mono.just(new HashMap<>()));
    Assertions.assertNotNull(
        redissonCombinationRepository.getCombinations(new HashSet<>(Arrays.asList("abc", "def"))));
  }
}
