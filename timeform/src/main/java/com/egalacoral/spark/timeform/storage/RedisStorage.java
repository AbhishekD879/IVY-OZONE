package com.egalacoral.spark.timeform.storage;

import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import org.redisson.RedissonMapCache;
import org.redisson.api.RLock;
import org.redisson.api.RMapCache;
import org.redisson.api.RedissonClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class RedisStorage implements Storage {
  public static final TimeUnit DAYS = TimeUnit.DAYS;

  @Value("${redis.data.ttl.days}")
  public int ttlInDays = 2;

  private RedissonClient redissonClient;

  @Autowired
  public RedisStorage(RedissonClient redissonClient) {
    this.redissonClient = redissonClient;
  }

  @Override
  public <E> Set<E> getSet(String name) {
    return redissonClient.getSet(name);
  }

  @Override
  public <E> List<E> getList(String name) {
    return redissonClient.getList(name);
  }

  @Override
  public <K, V> Map<K, V> getMap(String name) {
    RMapCache<K, V> mapCache = redissonClient.getMapCache(name);
    return new RMapCacheAdapter<>((RedissonMapCache) mapCache, ttlInDays, DAYS);
  }

  @Override
  public RLock getLock(String key) {
    return redissonClient.getLock(key);
  }
}
