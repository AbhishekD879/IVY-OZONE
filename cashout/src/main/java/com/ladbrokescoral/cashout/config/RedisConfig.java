package com.ladbrokescoral.cashout.config;

import static io.lettuce.core.ReadFrom.ANY;

import com.ladbrokescoral.cashout.model.RedisSaverLock;
import com.ladbrokescoral.cashout.model.context.SelectionPrice;
import com.ladbrokescoral.cashout.repository.EntityStatus;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.ReactiveRedisConnectionFactory;
import org.springframework.data.redis.connection.RedisStaticMasterReplicaConfiguration;
import org.springframework.data.redis.connection.lettuce.LettuceClientConfiguration;
import org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory;
import org.springframework.data.redis.core.ReactiveRedisTemplate;
import org.springframework.data.redis.serializer.Jackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.RedisSerializationContext;
import org.springframework.data.redis.serializer.StringRedisSerializer;

@Configuration
public class RedisConfig {

  @Bean
  @ConditionalOnProperty(name = "spring.redis.read.host")
  public LettuceConnectionFactory redisConnectionFactory(
      @Value("${spring.redis.host}") String primaryHost,
      @Value("${spring.redis.read.host:localhost}") String readHost,
      @Value("${spring.redis.port}") int port) {

    LettuceClientConfiguration clientConfig =
        LettuceClientConfiguration.builder().readFrom(ANY).build();

    RedisStaticMasterReplicaConfiguration serverConfig =
        new RedisStaticMasterReplicaConfiguration(primaryHost, port);

    if (!primaryHost.equals(readHost) && !readHost.equals("localhost")) {
      serverConfig.addNode(readHost, port);
    }

    return new LettuceConnectionFactory(serverConfig, clientConfig);
  }

  @Bean
  RedisSerializationContext<String, SelectionPrice> serializationSelectionPriceContext() {
    return RedisSerializationContext.<String, SelectionPrice>newSerializationContext()
        .hashKey(new StringRedisSerializer())
        .hashValue(new Jackson2JsonRedisSerializer<>(SelectionPrice.class))
        .key(new StringRedisSerializer())
        .value(new Jackson2JsonRedisSerializer<>(SelectionPrice.class))
        .build();
  }

  @Bean
  RedisSerializationContext<String, EntityStatus> entitytStatusSerializationCtx() {
    return RedisSerializationContext.<String, EntityStatus>newSerializationContext()
        .hashKey(new StringRedisSerializer())
        .hashValue(new Jackson2JsonRedisSerializer<>(EntityStatus.class))
        .key(new StringRedisSerializer())
        .value(new Jackson2JsonRedisSerializer<>(EntityStatus.class))
        .build();
  }

  @Bean
  ReactiveRedisTemplate<String, EntityStatus> entityStatusReactiveRedisTemplate(
      ReactiveRedisConnectionFactory redisConnectionFactory,
      RedisSerializationContext<String, EntityStatus> entitytStatusSerializationCtx) {
    return new ReactiveRedisTemplate<>(redisConnectionFactory, entitytStatusSerializationCtx);
  }

  @Bean
  ReactiveRedisTemplate<String, SelectionPrice> reactiveRedisSelectionPriceTemplate(
      ReactiveRedisConnectionFactory redisConnectionFactory,
      RedisSerializationContext<String, SelectionPrice> serializationSelectionPriceContext) {
    return new ReactiveRedisTemplate<>(redisConnectionFactory, serializationSelectionPriceContext);
  }

  @Bean
  RedisSerializationContext<String, RedisSaverLock> serializationLockContext() {
    return RedisSerializationContext.<String, RedisSaverLock>newSerializationContext()
        .hashKey(new StringRedisSerializer())
        .hashValue(new Jackson2JsonRedisSerializer<>(RedisSaverLock.class))
        .key(new StringRedisSerializer())
        .value(new Jackson2JsonRedisSerializer<>(RedisSaverLock.class))
        .build();
  }

  @Bean
  ReactiveRedisTemplate<String, RedisSaverLock> reactiveRedisLockTemplate(
      ReactiveRedisConnectionFactory redisConnectionFactory,
      RedisSerializationContext<String, RedisSaverLock> serializationSelectionPriceContext) {
    return new ReactiveRedisTemplate<>(redisConnectionFactory, serializationSelectionPriceContext);
  }
}
