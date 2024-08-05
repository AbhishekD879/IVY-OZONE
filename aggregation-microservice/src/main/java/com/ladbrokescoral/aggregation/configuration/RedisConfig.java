package com.ladbrokescoral.aggregation.configuration;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.ReactiveRedisConnectionFactory;
import org.springframework.data.redis.core.ReactiveRedisTemplate;
import org.springframework.data.redis.repository.configuration.EnableRedisRepositories;
import org.springframework.data.redis.serializer.GenericToStringSerializer;
import org.springframework.data.redis.serializer.RedisSerializationContext;
import org.springframework.data.redis.serializer.StringRedisSerializer;

@Configuration
@EnableRedisRepositories
public class RedisConfig {

  @Bean
  RedisSerializationContext<String, byte[]> serializationPathContext() {
    return RedisSerializationContext.<String, byte[]>newSerializationContext()
        .hashKey(new StringRedisSerializer())
        .hashValue(new GenericToStringSerializer<>(byte[].class))
        .key(new StringRedisSerializer())
        .value(new GenericToStringSerializer<>(byte[].class))
        .build();
  }

  @Bean
  ReactiveRedisTemplate<String, byte[]> reactiveRedisPathTemplate(
      ReactiveRedisConnectionFactory redisConnectionFactory,
      RedisSerializationContext<String, byte[]> serializationPathContext) {
    return new ReactiveRedisTemplate<>(redisConnectionFactory, serializationPathContext);
  }
}
