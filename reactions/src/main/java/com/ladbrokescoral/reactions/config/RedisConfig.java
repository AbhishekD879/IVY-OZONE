package com.ladbrokescoral.reactions.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.ReactiveRedisConnectionFactory;
import org.springframework.data.redis.core.ReactiveRedisOperations;
import org.springframework.data.redis.core.ReactiveRedisTemplate;
import org.springframework.data.redis.repository.configuration.EnableRedisRepositories;
import org.springframework.data.redis.serializer.Jackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.RedisSerializationContext;
import org.springframework.data.redis.serializer.StringRedisSerializer;

/**
 * @author PBalarangakumar 15-06-2023
 */
@Configuration
@EnableRedisRepositories
public class RedisConfig {

  @Bean
  ReactiveRedisOperations<String, Object> reactiveRedisOperations(
      ReactiveRedisConnectionFactory redisConnectionFactory) {
    Jackson2JsonRedisSerializer<Object> serializer =
        new Jackson2JsonRedisSerializer<>(Object.class);

    RedisSerializationContext.RedisSerializationContextBuilder<String, Object> builder =
        RedisSerializationContext.newSerializationContext(new StringRedisSerializer());
    RedisSerializationContext<String, Object> serializationPathContext =
        builder.value(serializer).build();

    return new ReactiveRedisTemplate<>(redisConnectionFactory, serializationPathContext);
  }
}
