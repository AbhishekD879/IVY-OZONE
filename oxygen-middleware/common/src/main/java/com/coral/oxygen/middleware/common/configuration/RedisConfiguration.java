package com.coral.oxygen.middleware.common.configuration;

import com.coral.oxygen.middleware.common.exceptions.InvalidConfigurationException;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.redisson.Redisson;
import org.redisson.api.RedissonClient;
import org.redisson.config.Config;
import org.redisson.config.ReadMode;
import org.redisson.config.SentinelServersConfig;
import org.redisson.config.SingleServerConfig;
import org.redisson.spring.data.connection.RedissonConnectionFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.actuate.redis.RedisHealthIndicator;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;

@Slf4j
@Configuration
public class RedisConfiguration {
  private static final int SCAN_INTERVAL = 5000;

  @Bean
  @ConditionalOnProperty(
      prefix = "redisson.redis.sentinel",
      value = "mode",
      havingValue = "true",
      matchIfMissing = false)
  public Config getSentinelServerConfig(
      @Value("${redisson.redis.sentinel.master}") String master,
      @Value("${redisson.redis.sentinel.nodes}") String nodes,
      @Value("${redisson.redis.password}") String password,
      @Value("${redisson.redis.sentinel.check:true}") boolean checkSentinels) {
    log.info("REDIS_SENTINEL_MASTER_NAME and checkSentinels = {}, {}", master, checkSentinels);
    Config config = new Config();
    SentinelServersConfig serversConfig = config.useSentinelServers();
    serversConfig.setMasterName(master);
    serversConfig.setReadMode(ReadMode.SLAVE);
    serversConfig.setCheckSentinelsList(checkSentinels);
    if (StringUtils.isEmpty(nodes)) {
      log.error("Please provide redis sentinel servers in property REDIS_SENTINEL_SERVERS");
      throw new InvalidConfigurationException(
          "Please provide redis sentinel servers in property REDIS_SENTINEL_SERVERS");
    } else {
      String[] sentinelNodes = nodes.split(",");
      serversConfig.addSentinelAddress(sentinelNodes).setScanInterval(SCAN_INTERVAL);
      if (StringUtils.isNotEmpty(password)) {
        serversConfig.setPassword(password);
      }
      log.info("REDIS_SENTINEL_SERVERS = {}", nodes);
    }
    return config;
  }

  @Bean
  @ConditionalOnProperty(
      prefix = "redisson.redis.sentinel",
      value = "mode",
      havingValue = "false",
      matchIfMissing = false)
  public Config getSingleServerConfig(
      @Value("${spring.redis.host:localhost}") String host,
      @Value("${spring.redis.port:6379}") Integer port) {
    Config redissonConfig = new Config();
    SingleServerConfig serverConfig = redissonConfig.useSingleServer();
    serverConfig.setAddress(String.format("redis://%s:%s", host, port));
    return redissonConfig;
  }

  @Bean
  public RedissonClient redissonClient(Config redissonConfig) {
    return Redisson.create(redissonConfig);
  }

  @Bean
  public RedisConnectionFactory redissonConnectionFactory(RedissonClient redissonClient) {
    return new RedissonConnectionFactory(redissonClient);
  }

  @Bean
  public RedisTemplate<String, Object> redisTemplate(
      RedisConnectionFactory redisConnectionFactory) {
    RedisTemplate<String, Object> template = new RedisTemplate<>();
    template.setConnectionFactory(redisConnectionFactory);
    template.afterPropertiesSet();
    return template;
  }

  @Bean
  public StringRedisTemplate stringRedisTemplate(RedisConnectionFactory redisConnectionFactory) {
    return new StringRedisTemplate(redisConnectionFactory);
  }

  @Bean
  public RedisHealthIndicator redisHealthIndicator(
      RedissonConnectionFactory redissonConnectionFactory) {
    return new RedisHealthIndicator(redissonConnectionFactory);
  }
}
