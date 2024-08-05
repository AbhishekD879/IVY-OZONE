package com.egalacoral.spark.liveserver;

import java.util.Map;

public interface Subscriber {
  void subscribeOnClock(String eventId);

  void subscribeOnEvent(String eventId, int categoryId);

  void subscribeOnMarket(String marketId, String eventId);

  void subscribeOnScore(String eventId);

  void subscribeOnSelection(String selectionId, String eventId);

  Map<String, SubscriptionSubject> getPayloadItems();
}
