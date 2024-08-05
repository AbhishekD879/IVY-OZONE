package com.coral.oxygen.middleware.ms.quickbet.configuration;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.vavr.jackson.datatype.VavrModule;
import org.springframework.boot.autoconfigure.data.redis.RedisProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisKeyValueAdapter;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.repository.configuration.EnableRedisRepositories;
import org.springframework.data.redis.serializer.Jackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.RedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;

/**
 * @author volodymyr.masliy
 */
@Configuration
@EnableRedisRepositories(
    basePackages = {"com.coral.oxygen.middleware.ms.quickbet"},
    enableKeyspaceEvents = RedisKeyValueAdapter.EnableKeyspaceEvents.ON_STARTUP,
    keyspaceNotificationsConfigParameter = "")
@EnableConfigurationProperties(RedisProperties.class)
@Profile("!UNIT")
public class SessionStorageConfiguration {

  @Bean
  public RedisTemplate<String, SessionDto> redisTemplate(RedisConnectionFactory connectionFactory) {
    RedisTemplate<String, SessionDto> redisTemplate = new RedisTemplate<>();
    redisTemplate.setConnectionFactory(connectionFactory);
    Jackson2JsonRedisSerializer<SessionDto> serializer =
        new Jackson2JsonRedisSerializer<>(SessionDto.class);
    serializer.setObjectMapper(new ObjectMapper().registerModule(new VavrModule()));
    RedisSerializer<String> stringRedisSerializer = new StringRedisSerializer();
    redisTemplate.setKeySerializer(stringRedisSerializer);
    redisTemplate.setValueSerializer(serializer);
    redisTemplate.setHashKeySerializer(stringRedisSerializer);
    redisTemplate.setHashValueSerializer(serializer);
    redisTemplate.afterPropertiesSet();
    return redisTemplate;
  }
}
