package com.coral.oxygen.middleware.ms.liveserv.model;

import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import com.github.benmanes.caffeine.cache.RemovalCause;
import com.github.benmanes.caffeine.cache.Scheduler;
import java.time.Duration;
import java.util.Collection;
import java.util.Collections;
import java.util.Map;
import java.util.concurrent.ScheduledExecutorService;
import java.util.function.BiConsumer;

public class CacheSubscriptionStatsMapImpl implements SubscriptionStatsMap {
  private final Cache<String, SubscriptionStats> subscriptions;

  public CacheSubscriptionStatsMapImpl(
      long maxItemsCount,
      Duration itemTtl,
      BiConsumer<String, SubscriptionStats> onDelete,
      ScheduledExecutorService scheduledExecutor) {
    this.subscriptions =
        Caffeine.newBuilder()
            .maximumSize(maxItemsCount)
            .expireAfterWrite(itemTtl)
            .scheduler(Scheduler.forScheduledExecutorService(scheduledExecutor))
            .removalListener(
                (String channel, SubscriptionStats stats, RemovalCause cause) -> {
                  // Ignore the «Entry replaced» event notification.
                  if (!RemovalCause.REPLACED.equals(cause)) {
                    onDelete.accept(channel, stats);
                  }
                })
            .build();
  }

  @Override
  public Map<String, SubscriptionStats> asMap() {
    return Collections.unmodifiableMap(subscriptions.asMap());
  }

  @Override
  public int size() {
    return (int) subscriptions.estimatedSize();
  }

  @Override
  public SubscriptionStats get(Object key) {
    return subscriptions.getIfPresent(key);
  }

  @Override
  public void put(String key, SubscriptionStats value) {
    subscriptions.put(key, value);
  }

  @Override
  public SubscriptionStats remove(Object key) {
    SubscriptionStats storedValue = get(key);
    subscriptions.invalidate(key);
    return storedValue;
  }

  @Override
  public void clear() {
    subscriptions.invalidateAll();
  }

  @Override
  public Collection<SubscriptionStats> values() {
    return asMap().values();
  }
}
