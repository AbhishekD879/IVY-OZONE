package com.coral.oxygen.middleware.ms.quickbet.configuration;

import java.util.Arrays;
import java.util.List;
import lombok.Setter;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.redisson.Redisson;
import org.redisson.api.RedissonClient;
import org.redisson.config.Config;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/*
     Redisson client is used for the Locking the objects and etc.,
*/

@Configuration
@Setter
public class RedissonConfiguration {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Value("${redis.sentinel.configuration.enable:false}")
  private boolean useSentinelConfiguration;

  @Value("${spring.redis.sentinel.master:null}")
  private String sentinelMaster;

  @Value("${spring.redis.sentinel.nodes:null}")
  private String sentinelNodes;

  @Value("${spring.redis.password:null}")
  private String redisPassword;

  @Value("${remote-betslip.elasticache.host}")
  private String singleNodeHost;

  @Value("${remote-betslip.elasticache.port}")
  private int singleNodePort;

  @Value("${redis.password.enable:false}")
  private boolean usePassword;

  private static final String REDIS = "redis://";

  @Bean
  public Config config() {
    Config config = new Config();
    if (useSentinelConfiguration) {
      List<String> sentinelAddresses = createSentinelNodeAddress(sentinelNodes);
      config
          .useSentinelServers()
          .setMasterName(sentinelMaster)
          .addSentinelAddress(sentinelAddresses.stream().toArray(String[]::new))
          .setPassword(redisPassword);
    } else {
      if (usePassword) {
        config
            .useSingleServer()
            .setAddress(REDIS + singleNodeHost + ":" + singleNodePort)
            .setPassword(redisPassword);
      } else {
        config.useSingleServer().setAddress(REDIS + singleNodeHost + ":" + singleNodePort);
      }
    }
    return config;
  }

  public List<String> createSentinelNodeAddress(String redisSentinelNodes) {
    String[] addresses = redisSentinelNodes.trim().split(",");
    return Arrays.stream(addresses).map(String::trim).map(address -> REDIS + address).toList();
  }

  @Bean
  public RedissonClient redissonClient(Config config) {
    return Redisson.create(config);
  }
}
