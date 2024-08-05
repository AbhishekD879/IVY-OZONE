package com.coral.oxygen.middleware.common.imdg;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;

/**
 * @author volodymyr.masliy
 */
public interface DistributedLock extends Lock {
  boolean tryLock(long time, long leaseTime, TimeUnit leaseUnit) throws InterruptedException;

  boolean isLockedByCurrentThread();

  void forceUnlock();
}
