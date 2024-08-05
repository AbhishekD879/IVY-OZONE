package com.ladbrokescoral.reactions.repository.redis;

import java.util.List;
import java.util.Map;
import org.springframework.data.redis.connection.ReactiveRedisConnectionFactory;
import org.springframework.data.redis.core.ReactiveRedisOperations;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 16-06-2023
 */
@Component
public class RedisOperations {

  private final ReactiveRedisOperations<String, String> reactiveRedisOperations;
  private final ReactiveRedisConnectionFactory reactiveRedisConnectionFactory;

  public RedisOperations(
      final ReactiveRedisOperations<String, String> reactiveRedisOperations,
      final ReactiveRedisConnectionFactory reactiveRedisConnectionFactory) {
    this.reactiveRedisOperations = reactiveRedisOperations;
    this.reactiveRedisConnectionFactory = reactiveRedisConnectionFactory;
  }

  public Mono<Boolean> set(final String key, final String value) {
    return reactiveRedisOperations.opsForValue().set(key, value);
  }

  public Mono<String> get(final String key) {
    return reactiveRedisOperations.opsForValue().get(key);
  }

  public Mono<Long> increment(final String key) {
    return reactiveRedisOperations.opsForValue().increment(key);
  }

  public Mono<String> getAndSet(final String key, final String value) {
    return reactiveRedisOperations.opsForValue().getAndSet(key, value);
  }

  public Mono<Long> decrement(final String key) {
    return reactiveRedisOperations.opsForValue().decrement(key);
  }

  public Mono<List<String>> multiGet(final List<String> keys) {
    return reactiveRedisOperations.opsForValue().multiGet(keys);
  }

  public Mono<Boolean> multiSet(final Map<String, String> userKeys) {
    return reactiveRedisOperations.opsForValue().multiSet(userKeys);
  }

  public Mono<String> cleanUpAllRedisKeys() {
    return reactiveRedisConnectionFactory.getReactiveConnection().serverCommands().flushAll();
  }
}
