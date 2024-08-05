package com.egalacoral.spark.timeform.storage;

import java.util.Collection;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import org.redisson.RedissonMapCache;

public class RMapCacheAdapter<K, V> implements Map<K, V> {

  private RedissonMapCache<K, V> redissonMapCache;
  private int ttlInMinuites;
  private TimeUnit timeUnit;

  public RMapCacheAdapter(RedissonMapCache redissonMapCache, int ttl, TimeUnit timeUnit) {
    this.redissonMapCache = redissonMapCache;
    this.ttlInMinuites = ttl;
    this.timeUnit = timeUnit;
  }

  @Override
  public int size() {
    return redissonMapCache.size();
  }

  @Override
  public boolean isEmpty() {
    return redissonMapCache.isEmpty();
  }

  @Override
  public boolean containsKey(Object key) {
    return redissonMapCache.containsKey(key);
  }

  @Override
  public boolean containsValue(Object value) {
    return redissonMapCache.containsValue(value);
  }

  @Override
  public V get(Object key) {
    return redissonMapCache.get(key);
  }

  @Override
  public V put(K key, V value) {
    //    return redissonMapCache.put(key, value);
    return redissonMapCache.put(key, value, ttlInMinuites, timeUnit);
  }

  @Override
  public V remove(Object key) {
    return redissonMapCache.remove(key);
  }

  @Override
  public void putAll(Map<? extends K, ? extends V> m) {
    m.entrySet().stream().forEach(e -> put(e.getKey(), e.getValue()));
  }

  @Override
  public void clear() {
    redissonMapCache.clear();
  }

  @Override
  public Set<K> keySet() {
    return redissonMapCache.keySet();
  }

  @Override
  public Collection<V> values() {
    return redissonMapCache.values();
  }

  @Override
  public Set<Entry<K, V>> entrySet() {
    return redissonMapCache.entrySet();
  }
}
