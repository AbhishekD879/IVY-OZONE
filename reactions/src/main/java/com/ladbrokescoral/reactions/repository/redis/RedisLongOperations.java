package com.ladbrokescoral.reactions.repository.redis;

import java.util.Map;
import org.springframework.data.redis.core.ReactiveRedisOperations;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 19-06-2023
 */
@Component
public class RedisLongOperations {

  private final ReactiveRedisOperations<String, Object> reactiveRedisOperations;

  public RedisLongOperations(
      final ReactiveRedisOperations<String, Object> reactiveRedisOperations) {
    this.reactiveRedisOperations = reactiveRedisOperations;
  }

  public Mono<Boolean> multiSet(final Map<String, Long> userInfo) {
    return reactiveRedisOperations.opsForValue().multiSet(userInfo);
  }
}
