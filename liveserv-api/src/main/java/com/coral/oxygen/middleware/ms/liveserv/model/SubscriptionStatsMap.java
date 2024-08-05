package com.coral.oxygen.middleware.ms.liveserv.model;

import java.util.Collection;
import java.util.Map;

public interface SubscriptionStatsMap {

  void put(String channel, SubscriptionStats stats);

  SubscriptionStats get(Object channel);

  SubscriptionStats remove(Object channel);

  Collection<SubscriptionStats> values();

  Map<String, SubscriptionStats> asMap();

  int size();

  void clear();
}
