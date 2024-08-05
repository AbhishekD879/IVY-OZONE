package com.ladbrokescoral.reactions.health;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;
import static org.springframework.boot.actuate.health.Status.*;

import io.lettuce.core.RedisException;
import java.util.Properties;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.boot.actuate.health.Health;
import org.springframework.data.redis.connection.ReactiveRedisConnection;
import org.springframework.data.redis.connection.ReactiveRedisConnectionFactory;
import org.springframework.data.redis.connection.ReactiveServerCommands;
import reactor.core.publisher.Mono;

class RedisHealthIndicatorTest {
  private ReactiveRedisConnectionFactory redisConnectionFactory;

  private ReactiveRedisConnection redisConnection;

  private ReactiveServerCommands serverCommands;

  private RedisHealthIndicator redisHealthIndicator;

  @BeforeEach
  void setUp() {
    redisConnectionFactory = Mockito.mock(ReactiveRedisConnectionFactory.class);
    redisConnection = mock(ReactiveRedisConnection.class);
    redisHealthIndicator = new RedisHealthIndicator(redisConnectionFactory);
    serverCommands = mock(ReactiveServerCommands.class);
  }

  @Test
  void testDoHealthCheckRedisIsUp_() {
    Properties redisInfoProperties = new Properties();
    redisInfoProperties.put("redis_version", "6.0.9");
    redisInfoProperties.put("uptime_in_seconds", "12345");
    redisInfoProperties.put("used_memory", "1024000");
    when(redisConnectionFactory.getReactiveConnection()).thenReturn(redisConnection);
    when(redisConnection.serverCommands()).thenReturn(serverCommands);
    when(serverCommands.info()).thenReturn(Mono.just(redisInfoProperties));
    Health health = redisHealthIndicator.health().block();
    assertEquals(UP, health.getStatus());
  }

  @Test
  void testDoHealthCheckRedisIsEmpty_() {
    when(redisConnectionFactory.getReactiveConnection()).thenReturn(redisConnection);
    when(redisConnection.serverCommands()).thenReturn(serverCommands);
    when(serverCommands.info()).thenReturn(Mono.empty());
    Health health = redisHealthIndicator.health().block();
    assertEquals(DOWN, health.getStatus());
  }

  @Test
  void testDoHealthCheckRedisWithException_() {
    when(redisConnectionFactory.getReactiveConnection()).thenReturn(redisConnection);
    when(redisConnection.serverCommands()).thenReturn(serverCommands);
    when(serverCommands.info()).thenReturn(Mono.error(new RedisException("Could not ping Redis.")));
    Health health = redisHealthIndicator.health().block();
    assertEquals(DOWN, health.getStatus());
  }
}
