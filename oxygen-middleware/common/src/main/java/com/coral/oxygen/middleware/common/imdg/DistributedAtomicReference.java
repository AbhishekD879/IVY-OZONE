package com.coral.oxygen.middleware.common.imdg;

/**
 * @author volodymyr.masliy
 */
public interface DistributedAtomicReference<T> {
  T get();

  void set(T currentNodeIdentificator);
}
