package com.ladbrokescoral.oxygen.trendingbets.context;

import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import com.github.benmanes.caffeine.cache.RemovalCause;
import com.github.benmanes.caffeine.cache.Scheduler;
import java.time.Duration;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.Executors;
import java.util.function.BiConsumer;
import java.util.function.Function;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@AllArgsConstructor
@Slf4j
public class PersonalizedBetsMap<K, V> implements TrendingEventMap<K, V> {

  private Cache<K, V> personalizedBets;

  public PersonalizedBetsMap(long maxItemsCount, Duration itemTtl, BiConsumer<K, V> onDelete) {
    this.personalizedBets =
        Caffeine.newBuilder()
            .maximumSize(maxItemsCount)
            .expireAfterWrite(itemTtl)
            .scheduler(Scheduler.forScheduledExecutorService(Executors.newScheduledThreadPool(1)))
            .removalListener(
                (K channel, V trendingEvents, RemovalCause cause) -> {
                  log.info("cause for delete :: {}", cause);

                  if (RemovalCause.EXPIRED.equals(cause) || RemovalCause.SIZE.equals(cause)) {
                    onDelete.accept(channel, trendingEvents);
                  }
                })
            .build();
  }

  @Override
  public void put(K var1, V var2) {
    personalizedBets.put(var1, var2);
  }

  @Override
  public V get(K key) {
    return this.personalizedBets.getIfPresent(key);
  }

  @Override
  public V remove(K liveServChannel) {
    V storedValue = this.get(liveServChannel);
    this.personalizedBets.invalidate(liveServChannel);
    return storedValue;
  }

  @Override
  public void computeIfAbsent(K channel, Function<? super K, ? extends V> mappingFunction) {
    if (get(channel) == null) {
      put(channel, mappingFunction.apply(channel));
    }
  }

  @Override
  public Set<K> keySet() {
    return personalizedBets.asMap().keySet();
  }

  @Override
  public void clear() {
    this.personalizedBets.invalidateAll();
  }

  @Override
  public int size() {
    return (int) personalizedBets.estimatedSize();
  }

  @Override
  public Set<Map.Entry<K, V>> entrySet() {
    return personalizedBets.asMap().entrySet();
  }
}
