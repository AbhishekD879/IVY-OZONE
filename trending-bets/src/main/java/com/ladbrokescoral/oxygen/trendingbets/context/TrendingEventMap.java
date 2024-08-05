package com.ladbrokescoral.oxygen.trendingbets.context;

import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.function.Function;

public interface TrendingEventMap<K, V> {

  void put(K key, V value);

  V get(K key);

  V remove(K key);

  void computeIfAbsent(K key, Function<? super K, ? extends V> mappingFunction);

  Set<K> keySet();

  void clear();

  int size();

  default V getOrDefault(K liveServChannel, V defaultValue) {
    return Optional.ofNullable(get(liveServChannel)).orElse(defaultValue);
  }

  Set<Map.Entry<K, V>> entrySet();
}
