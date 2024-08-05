package com.coral.oxygen.middleware.ms.liveserv.model;

import java.util.Collection;
import java.util.Map;

public class MapSubscriptionStatsMapImpl implements SubscriptionStatsMap {

  private final Map<String, SubscriptionStats> subscriptions;

  public MapSubscriptionStatsMapImpl(Map<String, SubscriptionStats> subscriptions) {
    this.subscriptions = subscriptions;
  }

  @Override
  public Collection<SubscriptionStats> values() {
    return subscriptions.values();
  }

  @Override
  public int size() {
    return subscriptions.size();
  }

  @Override
  public SubscriptionStats get(Object channel) {
    return subscriptions.get(channel);
  }

  @Override
  public void put(String channel, SubscriptionStats stats) {
    subscriptions.put(channel, stats);
  }

  @Override
  public SubscriptionStats remove(Object channel) {
    return subscriptions.remove(channel);
  }

  @Override
  public void clear() {
    subscriptions.clear();
  }

  @Override
  public Map<String, SubscriptionStats> asMap() {
    return subscriptions;
  }
}
