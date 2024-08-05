package com.ladbrokescoral.aggregation.repository;

import com.newrelic.api.agent.Trace;
import java.time.Duration;
import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.ReactiveRedisTemplate;
import org.springframework.data.redis.core.ReactiveValueOperations;
import reactor.core.publisher.Mono;

@Slf4j
public abstract class AbstractCacheImageRepository<K, T> implements CacheImageRepository<K, T> {

  private final ReactiveRedisTemplate<K, T> reactiveRedisTemplate;
  private final ReactiveValueOperations<K, T> valueOperations;

  private final Duration cacheTtl;

  protected AbstractCacheImageRepository(
      ReactiveRedisTemplate<K, T> reactiveRedisTemplate, Duration cacheTtl) {
    this.reactiveRedisTemplate = reactiveRedisTemplate;
    valueOperations = reactiveRedisTemplate.opsForValue();
    this.cacheTtl = cacheTtl;
  }

  @Override
  @Trace(metricName = "/Redis/Save/Image", async = true)
  public Mono<T> save(K key, T value) {
    log.debug("Save to cache key = {}", key);
    return valueOperations
        .set(buildKey(key), value)
        .map(status -> reactiveRedisTemplate.expire(buildKey(key), cacheTtl))
        .flatMap(status -> valueOperations.get(buildKey(key)));
  }

  @Override
  @Trace(metricName = "/Redis/Get/Single/Image", async = true)
  public Mono<T> get(K key) {
    log.debug("Get cache value for key = {}", key);
    return valueOperations.get(buildKey(key));
  }

  @Override
  @Trace(metricName = "/Redis/Get/Multiple/Images", async = true)
  public Mono<List<T>> multiGet(Collection<K> keys) {
    List<K> redisKeys = keys.stream().map(this::buildKey).collect(Collectors.toList());
    log.debug("Get cache value for keys = {}", keys);
    return valueOperations.multiGet(redisKeys);
  }

  @Override
  @Trace(metricName = "/Redis/Delete/Single/Image", async = true)
  public Mono<Boolean> delete(K key) {
    log.debug("Remove key from cache key = {}", key);
    return valueOperations.delete(buildKey(key));
  }

  private K buildKey(K key) {
    return key;
  }

  protected abstract String getKeyPrefix();
}
