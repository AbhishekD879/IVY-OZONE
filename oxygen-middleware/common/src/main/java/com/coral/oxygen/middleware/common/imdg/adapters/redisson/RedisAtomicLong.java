package com.coral.oxygen.middleware.common.imdg.adapters.redisson;

import com.coral.oxygen.middleware.common.imdg.DistributedAtomicLong;
import org.redisson.api.RAtomicLong;
import org.redisson.api.RedissonClient;

public class RedisAtomicLong implements DistributedAtomicLong {
  private RedissonClient redissonClient;
  private String name;

  RedisAtomicLong(RedissonClient redissonClient, String name) {
    this.redissonClient = redissonClient;
    this.name = name;
  }

  @Override
  public long addAndGet(long delta) {
    RAtomicLong atomicLong = redissonClient.getAtomicLong(name);
    return atomicLong.addAndGet(delta);
  }

  @Override
  public long get() {
    return redissonClient.getAtomicLong(name).get();
  }
}
