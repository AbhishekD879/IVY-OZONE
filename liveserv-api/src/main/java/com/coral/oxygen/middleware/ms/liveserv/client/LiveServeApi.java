package com.coral.oxygen.middleware.ms.liveserv.client;

import com.coral.oxygen.middleware.ms.liveserv.client.model.SubscriptionRequest;
import com.coral.oxygen.middleware.ms.liveserv.client.model.SubscriptionResponse;

public interface LiveServeApi {
  SubscriptionResponse subscribe(SubscriptionRequest subscription);
}
