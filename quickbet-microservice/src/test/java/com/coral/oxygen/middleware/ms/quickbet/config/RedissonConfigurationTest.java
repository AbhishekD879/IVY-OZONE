package com.coral.oxygen.middleware.ms.quickbet.config;

import com.coral.oxygen.middleware.ms.quickbet.configuration.RedissonConfiguration;
import java.util.List;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.redisson.config.Config;

class RedissonConfigurationTest {

  private RedissonConfiguration redissonConfiguration;

  @BeforeEach
  public void init() {
    redissonConfiguration = new RedissonConfiguration();
  }

  @Test
  void testSentinelPath() {

    String sentinelPath = "localhost:6379,localhost:6380,localhost:6378";

    List<String> sentinelPaths = redissonConfiguration.createSentinelNodeAddress(sentinelPath);

    Assertions.assertEquals(
        "[redis://localhost:6379, redis://localhost:6380, redis://localhost:6378]",
        sentinelPaths.toString());
  }

  @Test
  void testConfigForSentinelNode() {
    redissonConfiguration.setUseSentinelConfiguration(true);
    redissonConfiguration.setSentinelMaster("master");
    redissonConfiguration.setRedisPassword("hello");
    redissonConfiguration.setSentinelNodes("localhost:8903,localhost:5473");
    Config config = redissonConfiguration.config();
    Assertions.assertNotNull(config);
    Assertions.assertEquals("hello", config.useSentinelServers().getPassword());
  }

  @Test
  void testSingleNodeWithPassWord() {
    redissonConfiguration.setUsePassword(true);
    redissonConfiguration.setRedisPassword("hello");
    Config config = redissonConfiguration.config();
    Assertions.assertNotNull(config);
    Assertions.assertEquals("hello", config.useSingleServer().getPassword());
  }

  @Test
  void testSingleNodeConfigWithoutPassWord() {
    Config config = redissonConfiguration.config();
    Assertions.assertNotNull(config);
  }

  /*@Test(expected = RedisConnectionException.class)
  void testRedissonClient() {
    Config config = new Config();
    config.useSingleServer().setAddress("redis://127.0.0.1:6334");
    redissonConfiguration.redissonClient(config);
  }*/
}
