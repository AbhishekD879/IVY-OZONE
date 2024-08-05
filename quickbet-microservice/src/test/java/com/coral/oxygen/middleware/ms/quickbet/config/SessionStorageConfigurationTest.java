package com.coral.oxygen.middleware.ms.quickbet.config;

import com.coral.oxygen.middleware.ms.quickbet.configuration.SessionStorageConfiguration;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;

class SessionStorageConfigurationTest {

  private RedisConnectionFactory redisConnectionFactory;

  private SessionStorageConfiguration sessionStorageConfiguration;

  @BeforeEach
  public void init() {

    redisConnectionFactory = Mockito.mock(RedisConnectionFactory.class);

    sessionStorageConfiguration = new SessionStorageConfiguration();
  }

  @Test
  void testRedisTemplate() {

    RedisTemplate redisTemplate = sessionStorageConfiguration.redisTemplate(redisConnectionFactory);

    Assertions.assertNotNull(redisTemplate);
  }
}
