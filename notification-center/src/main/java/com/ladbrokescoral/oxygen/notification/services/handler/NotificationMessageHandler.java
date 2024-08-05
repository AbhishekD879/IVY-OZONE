package com.ladbrokescoral.oxygen.notification.services.handler;

public interface NotificationMessageHandler<T> {
  void handle(T message);
}
