package com.ladbrokescoral.reactions.config;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.mock;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.connection.ReactiveRedisConnectionFactory;
import org.springframework.data.redis.core.ReactiveRedisOperations;
import org.springframework.util.Assert;

@Disabled
@SpringBootTest
class RedisConfigTest {

  private ReactiveRedisOperations<String, String> reactiveRedisOperations;
  private ReactiveRedisConnectionFactory reactiveRedisConnectionFactory;

  @BeforeEach
  void setUp() {
    reactiveRedisOperations = Mockito.mock(ReactiveRedisOperations.class);
    reactiveRedisConnectionFactory = mock(ReactiveRedisConnectionFactory.class);
  }

  @Disabled("trying connect to redis")
  @Test
  void testReactiveRedisOperations() {
    assertNotNull(reactiveRedisOperations);
    Assert.notNull(reactiveRedisOperations, "ReactiveRedisOperations should not be null");
  }
}
