package com.ladbrokescoral.reactions.repository.redis;

import static org.mockito.Mockito.*;

import com.ladbrokescoral.reactions.exception.*;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.data.redis.connection.ReactiveRedisConnection;
import org.springframework.data.redis.connection.ReactiveRedisConnectionFactory;
import org.springframework.data.redis.connection.ReactiveServerCommands;
import org.springframework.data.redis.core.ReactiveRedisOperations;
import org.springframework.data.redis.core.ReactiveValueOperations;
import reactor.core.publisher.Mono;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class RedisOperationsTest {
  @InjectMocks RedisOperations redisOperations;

  ReactiveRedisOperations reactiveRedisOperations = Mockito.mock(ReactiveRedisOperations.class);

  ReactiveRedisConnectionFactory reactiveRedisConnectionFactory =
      Mockito.mock(ReactiveRedisConnectionFactory.class);
  @Mock ReactiveValueOperations<String, String> reactiveValueOperations;
  @Mock ReactiveRedisConnection reactiveRedisConnection;
  @Mock ReactiveServerCommands reactiveServerCommands;

  @Test
  void test() {
    Map<String, String> map = new HashMap<>();
    map.put("test", "test");
    when(reactiveRedisOperations.opsForValue()).thenReturn(reactiveValueOperations);
    when(reactiveRedisConnectionFactory.getReactiveConnection())
        .thenReturn(reactiveRedisConnection);
    when(reactiveRedisConnection.serverCommands()).thenReturn(reactiveServerCommands);
    when(reactiveServerCommands.flushAll()).thenReturn(Mono.just("test"));
    when(reactiveValueOperations.get("123")).thenReturn(Mono.just("value123"));
    when(reactiveValueOperations.set("123", "test")).thenReturn(Mono.just(true));
    when(reactiveValueOperations.increment("test")).thenReturn(Mono.just(10L));
    when(reactiveValueOperations.getAndSet("123", "test")).thenReturn(Mono.just("test"));
    when(reactiveValueOperations.decrement("test")).thenReturn(Mono.just(10L));
    when(reactiveValueOperations.multiGet(List.of("test"))).thenReturn(Mono.just(List.of("test")));
    when(reactiveValueOperations.multiSet(map)).thenReturn(Mono.just(true));
    redisOperations.get("123");
    redisOperations.set("test", "test");
    redisOperations.increment("test");
    redisOperations.getAndSet("123", "test");
    redisOperations.decrement("test");
    redisOperations.multiGet(List.of("test"));
    redisOperations.multiSet(map);
    Assert.assertNotNull(redisOperations.cleanUpAllRedisKeys());
    new BadRequestException("error", ErrorCode.SERVER_ERROR);
    new BadRequestException("error", ErrorCode.SERVER_ERROR, new Throwable());
    ServiceExecutionException exception = new ServiceExecutionException("error");
    exception.getErrorCode();
    UserNotFoundException exception1 = new UserNotFoundException("error");
    exception1.getErrorCode();
    ServiceUnavailableException exception2 =
        new ServiceUnavailableException("error", new Throwable());
    exception2.getErrorCode();
  }
}
