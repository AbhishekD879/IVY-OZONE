package com.egalacoral.spark.timeform.configuration;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.redisson.Redisson;
import org.redisson.api.RedissonClient;
import org.redisson.config.Config;
import org.redisson.config.TransportMode;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@Slf4j
public class RedissonConfiguration {

  @Value("${redis.sentinel.configuration.enable}")
  private boolean useSentinelConfiguration;

  @Value("${redis.connect.path}")
  private String redisConnectPath;

  @Value("${redis.sentinel.master}")
  private String sentinelMaster;

  @Value("${redis.sentinel.nodes}")
  private String sentinelNodes;

  @Value("${redis.password}")
  private String password;

  @Bean
  public Config getConfig() {
    Config config = new Config();
    config.setTransportMode(TransportMode.NIO);

    if (useSentinelConfiguration) {

      List<String> sentinelAddresses = createSentinelNodeAddress(sentinelNodes);
      log.info("Redis sentinel nodes : " + sentinelAddresses);

      config
          .useSentinelServers()
          .setMasterName(sentinelMaster)
          .addSentinelAddress(sentinelAddresses.stream().toArray(String[]::new))
          .setPassword(password);

    } else {
      config.useSingleServer().setAddress(redisConnectPath);
    }
    return config;
  }

  public List<String> createSentinelNodeAddress(String redisSentinelNodes) {
    String[] addresses = redisSentinelNodes.trim().split(",");

    return Arrays.stream(addresses)
        .map(address -> address.trim())
        .map(address -> "redis://" + address)
        .collect(Collectors.toList());
  }

  @Bean
  public RedissonClient getClient(Config config) {
    return Redisson.create(config);
  }
}
