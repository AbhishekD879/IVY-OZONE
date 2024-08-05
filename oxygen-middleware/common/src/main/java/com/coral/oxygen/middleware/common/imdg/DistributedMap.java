package com.coral.oxygen.middleware.common.imdg;

import java.util.Map;
import java.util.concurrent.ConcurrentMap;

/**
 * @author volodymyr.masliy
 */
public interface DistributedMap<K, V> extends ConcurrentMap<K, V> {
  void putAll(Map<? extends K, ? extends V> map);
}
