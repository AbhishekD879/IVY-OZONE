package com.ladbrokescoral.cashout.repository;

import com.ladbrokescoral.cashout.model.RedisSaverLock;
import com.newrelic.api.agent.Trace;
import org.springframework.data.redis.core.ReactiveRedisTemplate;
import org.springframework.data.redis.core.ReactiveValueOperations;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;

@Repository
public class LockRepository implements ReactiveLockRepository<RedisSaverLock> {

  public static final String REDIS_SAVER_LOCK = "REDIS_SAVER_LOCK";
  private final ReactiveValueOperations<String, RedisSaverLock> valueOperations;

  public LockRepository(ReactiveRedisTemplate<String, RedisSaverLock> reactiveRedisTemplate) {
    valueOperations = reactiveRedisTemplate.opsForValue();
  }

  @Trace(metricName = "/Redis/Save/Lock", async = true)
  @Override
  public Mono<RedisSaverLock> saveLock(String key, RedisSaverLock value) {
    return valueOperations
        .set(REDIS_SAVER_LOCK, value)
        .flatMap(status -> valueOperations.get(REDIS_SAVER_LOCK));
  }

  @Override
  @Trace(metricName = "/Redis/Get/Lock", async = true)
  public Mono<RedisSaverLock> getLock(String key) {
    return valueOperations.get(REDIS_SAVER_LOCK);
  }

  @Override
  @Trace(metricName = "/Redis/Delete/Lock", async = true)
  public Mono<Boolean> deleteLock(String key) {
    return valueOperations.delete(REDIS_SAVER_LOCK);
  }
}
