package com.entain.oxygen.betbuilder_middleware.config;

import static org.mockito.Mockito.*;

import com.entain.oxygen.betbuilder_middleware.repository.RedissonEventIdRepository;
import java.util.HashMap;
import java.util.Map;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mockito;
import org.redisson.api.*;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import reactor.core.publisher.Mono;

@ExtendWith(SpringExtension.class)
class RedissonEventRepositoryTest {
  @MockBean RLocalCachedMapReactive redissonEventIds;
  RMapReactive rMapReactive;
  RBatchReactive rBatchReactive;
  @MockBean RedissonReactiveClient redissonReactiveClient;
  @MockBean RedissonProperties redissonProperties;
  RedissonEventIdRepository redissonEventIdRepository;

  @BeforeEach
  void setUp() {
    when(redissonReactiveClient.getLocalCachedMap(Mockito.anyString(), Mockito.any()))
        .thenReturn(redissonEventIds);
    redissonEventIdRepository = new RedissonEventIdRepository(redissonReactiveClient);
    rBatchReactive = mock(RBatchReactive.class);
    rMapReactive = mock(RMapReactive.class);

    when(redissonReactiveClient.createBatch()).thenReturn(rBatchReactive);
    when(rBatchReactive.getMap("EventIDs_MAP")).thenReturn(rMapReactive);
  }

  @Test
  void testSaveEventIds() {
    BatchResult mockBatchResult = mock(BatchResult.class);

    when(rMapReactive.fastPutIfAbsent(Mockito.anyString(), Mockito.any()))
        .thenReturn(Mono.just(true));

    Mockito.when(rBatchReactive.execute()).thenReturn(Mono.just(mockBatchResult));

    Map<String, String> eventMap = new HashMap<>();
    eventMap.put("OeId1", "BeId1");
    eventMap.put("OeId2", "BeId2");
    redissonEventIdRepository.saveEvents(eventMap);
    Assertions.assertNotNull(eventMap);
  }

  @Test
  void testReadAllMap() {
    when(redissonEventIds.readAllMap()).thenReturn(Mono.just(new HashMap()));
    redissonEventIdRepository.readEvents();
    Assertions.assertNotNull(redissonEventIdRepository);
  }

  @Test
  void testDelete() {
    String key = "id";
    when(redissonEventIds.fastRemove(key)).thenReturn(Mono.just(true));
    redissonEventIdRepository.delete(key);
    Assertions.assertNotNull(key);
  }
}
