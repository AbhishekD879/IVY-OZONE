package com.egalacoral.spark.liveserver;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class SubscriptionSubjectFactory {
  public static SubscriptionSubject onEventSubscription(String eventId) {
    return new SubscriptionSubject(ChannelType.sEVENT, eventId);
  }

  public static SubscriptionSubject onMarketSubscription(String marketId) {
    return new SubscriptionSubject(ChannelType.sEVMKT, marketId);
  }

  public static SubscriptionSubject onSelectionSubscription(String selectionId) {
    return new SubscriptionSubject(ChannelType.sSELCN, selectionId);
  }

  public static SubscriptionSubject onScoreSubscription(String eventId) {
    return new SubscriptionSubject(ChannelType.sSCBRD, eventId);
  }

  public static SubscriptionSubject onAggregatedSubscription(String eventId) {
    return new SubscriptionSubject(ChannelType.SEVENT, eventId);
  }

  public static SubscriptionSubject onClockSubscription(String eventId) {
    return new SubscriptionSubject(ChannelType.sCLOCK, eventId);
  }
}
