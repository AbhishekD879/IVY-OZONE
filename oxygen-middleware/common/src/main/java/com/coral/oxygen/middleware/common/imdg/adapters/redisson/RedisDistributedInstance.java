package com.coral.oxygen.middleware.common.imdg.adapters.redisson;

import com.coral.oxygen.middleware.common.configuration.DistributedKey;
import com.coral.oxygen.middleware.common.imdg.DistributedAtomicLong;
import com.coral.oxygen.middleware.common.imdg.DistributedInstance;
import com.coral.oxygen.middleware.common.imdg.DistributedMap;
import com.coral.oxygen.middleware.common.imdg.DistributedProvider;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.redisson.api.RedissonClient;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.boot.actuate.redis.RedisHealthIndicator;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;

@Slf4j
public class RedisDistributedInstance implements DistributedInstance {
  private String prefix;
  private long defaultEntitiesTtl;
  private TimeUnit defaultEntriesTtlUnits;
  private RedissonClient redissonClient;
  private RedisTemplate<String, Object> redisTemplate;
  private StringRedisTemplate stringRedisTemplate;
  private RedisHealthIndicator redisHealthIndicator;

  public RedisDistributedInstance(
      RedisTemplate<String, Object> redisTemplate,
      StringRedisTemplate stringRedisTemplate,
      RedissonClient redissonClient,
      OxygenRedissonConfig config,
      RedisHealthIndicator redisHealthIndicator) {
    this.redissonClient = redissonClient;
    this.redisTemplate = redisTemplate;
    this.stringRedisTemplate = stringRedisTemplate;
    prefix = config.getPrefix();
    defaultEntitiesTtl = config.getMapEntriesTtl();
    defaultEntriesTtlUnits = config.getMapEntriesTtlUnits();
    this.redisHealthIndicator = redisHealthIndicator;
  }

  @Override
  public String getProviderName() {
    return DistributedProvider.REDIS_TEMPLATE.getName();
  }

  @Override
  public <K, V> DistributedMap<K, V> getMap(DistributedKey key) {
    log.info(
        "Get map {} [ttl: {}{}, max-size: unlimited]",
        key,
        defaultEntitiesTtl,
        defaultEntriesTtlUnits);
    return new RedissonCacheMap<>(
        redisTemplate.opsForHash(), getKeyName(key), defaultEntitiesTtl, defaultEntriesTtlUnits);
  }

  @Override
  public DistributedAtomicLong getAtomicLong(DistributedKey key) {
    return new RedisAtomicLong(redissonClient, getKeyName(key));
  }

  @Override
  public String getValue(DistributedKey key, String suffix) {
    return stringRedisTemplate.opsForValue().get(getKeyName(key, suffix));
  }

  @Override
  public String getValue(DistributedKey key) {
    return stringRedisTemplate.opsForValue().get(getKeyName(key));
  }

  @Override
  public List<String> getValues(DistributedKey key, List<String> suffixes) {
    List<String> keysToGet =
        suffixes.stream().map(k -> getKeyName(key, k)).collect(Collectors.toList());
    return stringRedisTemplate.opsForValue().multiGet(keysToGet);
  }

  @Override
  public String updateExpirableValue(DistributedKey key, String suffix, String newValue) {
    return updateStringValue(getKeyName(key, suffix), newValue);
  }

  @Override
  public String updateExpirableValue(DistributedKey key, String newValue) {
    return updateStringValue(getKeyName(key), newValue);
  }

  private String updateStringValue(String keyName, String newValue) {
    String oldValue = stringRedisTemplate.opsForValue().getAndSet(keyName, newValue);
    stringRedisTemplate.expire(keyName, defaultEntitiesTtl, defaultEntriesTtlUnits);
    return oldValue;
  }

  private String getKeyName(DistributedKey name, String key) {
    return String.join("-", getKeyName(name), key);
  }

  private String getKeyName(DistributedKey key) {
    return String.join("__", prefix, key.name());
  }

  @Override
  public HealthIndicator getHealthIndicator() {
    return redisHealthIndicator;
  }
}
