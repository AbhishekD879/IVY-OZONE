package com.ladbrokescoral.reactions.repository.redis;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.util.HashMap;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.data.redis.core.ReactiveRedisOperations;
import org.springframework.data.redis.core.ReactiveValueOperations;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

class RedisLongOperationsTest {

  private RedisLongOperations redisLongOperations;

  private ReactiveValueOperations<String, Object> stringObjectReactiveValueOperations;

  @Mock private ReactiveRedisOperations<String, Object> reactiveRedisOperations;

  @BeforeEach
  void setUp() {
    MockitoAnnotations.openMocks(this);
    redisLongOperations = new RedisLongOperations(reactiveRedisOperations);
    stringObjectReactiveValueOperations = mock(ReactiveValueOperations.class);
  }

  @Test
  void testMultiSet() {
    Map<String, Long> userInfo = new HashMap<>();
    userInfo.put("user1", 100L);
    userInfo.put("user2", 200L);
    when(reactiveRedisOperations.opsForValue()).thenReturn(stringObjectReactiveValueOperations);
    when(stringObjectReactiveValueOperations.multiSet(userInfo)).thenReturn(Mono.just(true));
    Mono<Boolean> resultMono = redisLongOperations.multiSet(userInfo);
    StepVerifier.create(resultMono).expectNext(true).expectComplete().verify();
  }
}
