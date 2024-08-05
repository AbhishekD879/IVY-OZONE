package com.coral.oxygen.edp.tracking;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/** Created by azayats on 22.12.17. */
public class InMemoryDataStorage<K, V> implements DataStorage<K, V> {

  private final Map<K, V> data;

  public InMemoryDataStorage() {
    this.data = new ConcurrentHashMap<>();
  }

  @Override
  public V get(K key) {
    return data.get(key);
  }

  @Override
  public V replace(K key, V value) {
    return data.put(key, value);
  }

  @Override
  public void remove(K key) {
    data.remove(key);
  }
}
