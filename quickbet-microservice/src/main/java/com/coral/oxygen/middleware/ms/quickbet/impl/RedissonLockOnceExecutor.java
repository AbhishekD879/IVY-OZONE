package com.coral.oxygen.middleware.ms.quickbet.impl;

import java.time.Duration;
import java.util.concurrent.TimeUnit;
import lombok.RequiredArgsConstructor;
import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@Profile("!UNIT")
public class RedissonLockOnceExecutor implements OnceExecutor {
  private final RedissonClient redisson;

  /**
   * Executes <code>action</code> only once in given <code>period</code> by locking on <code>
   * actionIdentity</code> If locked, <code>rejectedAction</code> will be executed instead.
   */
  @Override
  public void executeOnceDuringTimePeriod(
      String actionIdentity, Runnable action, Runnable rejectedAction, Duration period) {
    RLock lock = redisson.getFairLock(actionIdentity);

    if (lock.isLocked()) {
      rejectedAction.run();
      return;
    }

    try {
      // unlocks automatically after specified period of time
      lock.lock(period.getSeconds(), TimeUnit.SECONDS); // NOSONAR
      action.run();
    } finally {
      if (lock.isHeldByCurrentThread()) {
        lock.unlock();
      }
    }
  }
}
