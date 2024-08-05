package com.ladbrokescoral.oxygen.trendingbets.context;

import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import lombok.AllArgsConstructor;

@AllArgsConstructor
public class PopularBetsMap<K, V> implements TrendingEventMap<K, V> {

  private final Map<K, V> trendingSelections;

  @Override
  public void put(K key, V value) {
    trendingSelections.put(key, value);
  }

  @Override
  public V get(K var1) {
    return trendingSelections.get(var1);
  }

  @Override
  public V remove(K liveServChannel) {
    return trendingSelections.remove(liveServChannel);
  }

  @Override
  public void computeIfAbsent(K channel, Function<? super K, ? extends V> mappingFunction) {
    trendingSelections.computeIfAbsent(channel, mappingFunction);
  }

  @Override
  public Set<K> keySet() {
    return trendingSelections.keySet();
  }

  @Override
  public void clear() {
    trendingSelections.clear();
  }

  @Override
  public int size() {
    return trendingSelections.size();
  }

  @Override
  public Set<Map.Entry<K, V>> entrySet() {
    return trendingSelections.entrySet();
  }
}
