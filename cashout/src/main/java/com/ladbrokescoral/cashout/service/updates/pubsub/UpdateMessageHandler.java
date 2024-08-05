package com.ladbrokescoral.cashout.service.updates.pubsub;

public interface UpdateMessageHandler<T> {
  void handleUpdateMessage(T message);
}
