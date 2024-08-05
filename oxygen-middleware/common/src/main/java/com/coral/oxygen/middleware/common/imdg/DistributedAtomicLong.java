package com.coral.oxygen.middleware.common.imdg;

/**
 * @author volodymyr.masliy
 */
public interface DistributedAtomicLong {
  long addAndGet(long number);

  long get();
}
