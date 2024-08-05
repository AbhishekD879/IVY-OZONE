package com.coral.oxygen.middleware.ms.liveserv.model;

import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.Consumer;
import lombok.Data;

@Data
public class SubscriptionStats {

  private final String channel;

  private final long eventId;
  private Consumer<SubscriptionStats> onUnsubscribe;

  private String waterMark;

  private long updatesCount;

  private long lasSuccessUpdate;

  private long lastError;

  private int lastErrorsCount;

  private AtomicBoolean unsubscribeNotified = new AtomicBoolean();
  private AtomicBoolean expireNotified = new AtomicBoolean();

  public SubscriptionStats(String channel, long eventId) {
    this(
        channel,
        eventId,
        (SubscriptionStats s) -> {
          /* do nothing*/
        });
  }

  public SubscriptionStats(
      String channel, long eventId, Consumer<SubscriptionStats> onUnsubscribe) {
    this.channel = channel;
    this.eventId = eventId;
    this.onUnsubscribe = onUnsubscribe;
  }
}
