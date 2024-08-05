package com.coral.oxygen.middleware.common.imdg;

/**
 * @author volodymyr.masliy
 */
public interface DistributedTopic<T> {
  String getName();

  void publish(T message);
}
