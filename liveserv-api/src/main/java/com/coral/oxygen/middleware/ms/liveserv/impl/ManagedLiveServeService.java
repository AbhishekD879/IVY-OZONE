package com.coral.oxygen.middleware.ms.liveserv.impl;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import java.util.Map;

public interface ManagedLiveServeService extends LiveServService {

  int subscriptionsSize();

  void addSubscription(String channel, SubscriptionStats subscription);

  Map<String, SubscriptionStats> getSubscriptions();
}
