package com.entain.oxygen.betbuilder_middleware.config;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.redisson.config.Config;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@Import(RedissonProperties.class)
class RedissonConfigProviderTest {
  @Autowired RedissonProperties redissonProperties;
  private RedissonConfigProvider redissonConfigProvider;

  @BeforeEach
  public void init() {
    redissonProperties.setSentinel(true);
    redissonProperties.setSentinelMaster("betbuildermaster");
    redissonProperties.setSentinelNodes(
        "redis://at1t5xabmr001.dbz.unix:26396,redis://at1t5xabmr002.dbz.unix:26396");
    redissonConfigProvider = new RedissonConfigProvider(redissonProperties);
  }

  @Test
  void testGetSentinelServerConfig() {
    Config config = redissonConfigProvider.redissonConfig();
    assertTrue(
        config
            .useSentinelServers()
            .getSentinelAddresses()
            .contains("redis://at1t5xabmr001.dbz.unix:26396"));
    assertTrue(
        config
            .useSentinelServers()
            .getSentinelAddresses()
            .contains("redis://at1t5xabmr002.dbz.unix:26396"));
    assertEquals("betbuildermaster", config.useSentinelServers().getMasterName());
  }

  @Test
  void testGetSentinelServerBlankNodesConfig() {
    redissonProperties.setSentinelNodes("");
    Config config = redissonConfigProvider.redissonConfig();
    assertNotNull(config.useSentinelServers().getSentinelAddresses());
  }
}
