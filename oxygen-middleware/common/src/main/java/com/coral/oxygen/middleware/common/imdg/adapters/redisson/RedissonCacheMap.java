package com.coral.oxygen.middleware.common.imdg.adapters.redisson;

import com.coral.oxygen.middleware.common.imdg.DistributedMap;
import java.util.Collection;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import org.springframework.data.redis.core.HashOperations;

/**
 * @author taras.pelenskyi
 */
public class RedissonCacheMap<K, V> implements DistributedMap<K, V> {
  private final HashOperations<String, K, V> redisOperation;
  private final String name;
  private long ttl;
  private TimeUnit ttlUnits;

  RedissonCacheMap(
      HashOperations<String, K, V> redisOperation, String name, long ttl, TimeUnit ttlUnits) {
    this.redisOperation = redisOperation;
    this.name = name;
    this.ttl = ttl;
    this.ttlUnits = ttlUnits;
  }

  @Override
  public int size() {
    return Math.toIntExact(redisOperation.size(name));
  }

  @Override
  public boolean isEmpty() {
    return size() == 0;
  }

  @Override
  public boolean containsKey(Object key) {
    return redisOperation.hasKey(name, key);
  }

  @Override
  public boolean containsValue(Object value) {
    throw new UnsupportedOperationException("Redis containsValue: shouldn't be used");
  }

  @Override
  public V get(Object key) {
    return redisOperation.get(name, key);
  }

  // no possibilities to expire key in map
  // do we need old value here?
  @Override
  public V put(K key, V value) {
    V oldValue = get(key);
    redisOperation.put(name, key, value);
    expireIfSpecified();
    return oldValue;
  }

  // do we need old value here?
  @Override
  public V remove(Object key) {
    V oldValue = get(key);
    redisOperation.delete(name, key);
    return oldValue;
  }

  @Override
  public void putAll(Map<? extends K, ? extends V> map) {
    redisOperation.putAll(name, map);
    expireIfSpecified();
  }

  @Override
  public void clear() {
    redisOperation.getOperations().delete(name);
  }

  /**
   * @throws UnsupportedOperationException to indicate the method shouldn't be used
   */
  @Override
  public Set<K> keySet() {
    throw new UnsupportedOperationException("Redis keySet: shouldn't be used");
  }

  @Override
  public Collection<V> values() {
    throw new UnsupportedOperationException("Redis values: shouldn't be used");
  }

  @Override
  public Set<Entry<K, V>> entrySet() {
    // seems to be heavy opperation (used in DiagnosticControllerSpec test)
    return redisOperation.entries(name).entrySet();
  }

  @Override
  public V putIfAbsent(K key, V value) {
    V oldValue = get(key);
    redisOperation.putIfAbsent(name, key, value);
    expireIfSpecified();
    return oldValue;
  }

  @Override
  public boolean remove(Object key, Object value) {
    throw new UnsupportedOperationException(
        "Redis remove(Object key, Object value): shouldn't be used");
  }

  @Override
  public boolean replace(K key, V oldValue, V newValue) {
    throw new UnsupportedOperationException(
        "Redis replace(K key, V oldValue, V newValue): shouldn't be used");
  }

  @Override
  public V replace(K key, V value) {
    throw new UnsupportedOperationException("Redis replace(K key, V value): shouldn't be used");
  }

  private void expireIfSpecified() {
    if (ttl > 0 && Objects.nonNull(ttlUnits)) {
      redisOperation.getOperations().expire(name, ttl, ttlUnits);
    }
  }
}
