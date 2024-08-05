package com.coral.oxygen.middleware.ms.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import java.util.Map;

public interface LiveServService {
  void subscribe(String channel);

  void unsubscribe(String channel);

  Map<String, SubscriptionStats> getSubscriptions();
}
