package com.egalacoral.spark.timeform.service;

import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.concurrent.TimeUnit;
import java.util.function.Consumer;
import org.redisson.api.RLock;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class LockService {

  private static final transient Logger LOGGER = LoggerFactory.getLogger(LockService.class);

  private final Storage storage;

  @Autowired
  public LockService(Storage storage) {
    this.storage = storage;
  }

  public void doInLockOrSkip(String lockName, long leaseTime, Runnable runnable)
      throws InterruptedException {
    RLock lock = storage.getLock(lockName);
    boolean locked = false;
    locked = lock.tryLock(10, leaseTime, TimeUnit.MILLISECONDS);
    if (locked) {
      try {
        LOGGER.info("Locked {} ", lockName);
        runnable.run();
      } finally {
        lock.unlock();
        LOGGER.info("UnLocked {} ", lockName);
      }
    } else {
      LOGGER.info("Skipped as is Locked {} ", lockName);
    }
  }

  public void tryLockWithWrapper(
      String lockName, long leaseTime, Consumer<UnlockWrapper> consumer) {
    RLock lock = storage.getLock(lockName);
    boolean isLocked = false;
    try {

      isLocked = lock.tryLock(2, leaseTime, TimeUnit.SECONDS);
      if (isLocked) {
        LOGGER.info("{} lock was acquired", lock);
        UnlockWrapper wrapper = new UnlockWrapper(lock);
        try {
          consumer.accept(wrapper);
        } catch (Exception e) {
          LOGGER.error("Error occured in wrapper lock. Reason: {}", e.getMessage());
          wrapper.unlock();
        } finally {
          wrapper.close();
        }
      } else {
        LOGGER.info("{} already locked", lock);
      }
    } catch (InterruptedException e) {
      LOGGER.error("Could not take lock: {}", e.getMessage());
      Thread.currentThread().interrupt();
    }
  }

  public static class UnlockWrapper implements AutoCloseable {

    private final RLock lock;

    private volatile boolean unlocked = false;

    private volatile boolean unlockOnClose = true;

    public UnlockWrapper(RLock lock) {
      this.lock = lock;
    }

    public <T> DataCallback<T> wrap(DataCallback<T> callback) {
      unlockOnClose = false;
      return new DataCallback<T>() {

        @Override
        public void onResponse(T data) {
          try {
            callback.onResponse(data);
          } finally {
            unlock();
          }
        }

        @Override
        public void onError(Exception throwable) {
          unlock();
          callback.onError(throwable);
        }
      };
    }

    public void unlock() {
      if (!unlocked) {
        lock.forceUnlock();
        unlocked = true;
      }
    }

    @Override
    public void close() {
      if (unlockOnClose) {
        LOGGER.warn(
            "Unlocking in close method for locker {}. Maybe you forgot to wrap data callback.",
            lock.getName());
        unlock();
      }
    }
  }
}
