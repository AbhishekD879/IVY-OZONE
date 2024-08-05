package com.coral.oxygen.middleware.common.configuration;

import com.coral.oxygen.middleware.common.imdg.DistributedInstance;
import com.coral.oxygen.middleware.common.imdg.adapters.redisson.OxygenRedissonConfig;
import com.coral.oxygen.middleware.common.imdg.adapters.redisson.RedisDistributedInstance;
import java.util.concurrent.TimeUnit;
import org.redisson.api.RedissonClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.actuate.redis.RedisHealthIndicator;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;

/**
 * Used to select implementation of {@link
 * com.coral.oxygen.middleware.common.imdg.DistributedInstance}
 *
 * @author volodymyr.masliy
 */
@Configuration
public class DistributedInstanceConfiguration {

  @Bean
  DistributedInstance redisDistributedInstance(
      RedisTemplate<String, Object> redisTemplate,
      StringRedisTemplate stringRedisTemplate,
      RedissonClient redissonClient,
      OxygenRedissonConfig config,
      RedisHealthIndicator redisHealthIndicator) {
    return new RedisDistributedInstance(
        redisTemplate, stringRedisTemplate, redissonClient, config, redisHealthIndicator);
  }

  @Bean
  OxygenRedissonConfig redissonConfig(
      @Value("${distributed.prefix}") String prefix,
      @Value("${imdg.ttl.seconds}") long ttlSeconds) {
    return new OxygenRedissonConfig(prefix, ttlSeconds, TimeUnit.SECONDS);
  }
}
