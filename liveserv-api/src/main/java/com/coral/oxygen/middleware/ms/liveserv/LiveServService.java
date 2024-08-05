package com.coral.oxygen.middleware.ms.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import java.util.function.Consumer;

public interface LiveServService {
  void startConsuming();

  void stopConsuming() throws InterruptedException;

  void subscribe(String channel);

  void subscribe(String channel, Long eventId);

  void subscribe(String channel, Long eventId, Consumer<SubscriptionStats> onUnsubscribe);

  void unsubscribe(String channel);
}
