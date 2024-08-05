package com.entain.oxygen.betbuilder_middleware.config;

import java.util.Arrays;
import java.util.List;
import lombok.AllArgsConstructor;
import org.apache.commons.lang3.StringUtils;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.redisson.Redisson;
import org.redisson.api.RedissonClient;
import org.redisson.api.RedissonReactiveClient;
import org.redisson.config.Config;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@AllArgsConstructor
@EnableConfigurationProperties
public class RedissonConfigProvider {

  private final RedissonProperties redisProperties;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger();

  @Bean
  public Config redissonConfig() {
    return redisProperties.isSentinel() ? getSentinelServerConfig() : getSingleServerConfig();
  }

  @Bean
  public RedissonClient redissonClient(Config redissonConfig) {
    return Redisson.create(redissonConfig);
  }

  @Bean
  public RedissonReactiveClient redissonReactiveClient(RedissonClient redissonClient) {
    return redissonClient.reactive();
  }

  private Config getSentinelServerConfig() {
    Config config = new Config();
    List<String> sentinelAddresses = createSentinelAddress(redisProperties.getSentinelNodes());

    config
        .useSentinelServers()
        .setMasterName(redisProperties.getSentinelMaster())
        .setPassword(redisProperties.getPassword())
        .addSentinelAddress(sentinelAddresses.toArray(String[]::new));
    return config;
  }

  private Config getSingleServerConfig() {
    Config config = new Config();
    config
        .useSingleServer()
        .setDatabase(0)
        .setAddress(redisProperties.getSingleHost() + ":" + redisProperties.getSinglePort());
    return config;
  }

  private List<String> createSentinelAddress(String sentinelNodes) {
    if (StringUtils.isBlank(sentinelNodes)) {
      ASYNC_LOGGER.error("please provide the sentinel nodes information");
    }
    String[] addresses = sentinelNodes.trim().split(",");
    return Arrays.stream(addresses).map(String::trim).toList();
  }
}
