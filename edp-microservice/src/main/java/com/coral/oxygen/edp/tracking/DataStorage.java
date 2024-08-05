package com.coral.oxygen.edp.tracking;

/** Created by azayats on 18.12.17. */
public interface DataStorage<K, V> {

  V get(K key);

  V replace(K key, V value);

  void remove(K key);
}
