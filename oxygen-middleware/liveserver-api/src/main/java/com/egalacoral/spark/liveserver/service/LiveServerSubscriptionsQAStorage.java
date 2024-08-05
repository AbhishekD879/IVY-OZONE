package com.egalacoral.spark.liveserver.service;

import com.egalacoral.spark.liveserver.Message;
import com.egalacoral.spark.liveserver.SubscriptionSubject;
import java.util.Map;

public interface LiveServerSubscriptionsQAStorage {
  void storeActiveLiveServePayload(Map<String, SubscriptionSubject> liveservePayload);

  void storeLiveUpdateMessage(Message message);

  Map<String, Message> getMessages();

  Map<String, SubscriptionSubject> getSubscriptions();
}
