package com.coral.oxygen.middleware.ms.liveserv.client;

import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import java.util.Collection;
import java.util.List;

public interface LiveServerListener {

  void onMessages(List<Message> messages);

  void onError(Collection<SubscriptionStats> subscriptions, Throwable e);
}
