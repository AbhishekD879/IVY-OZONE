package com.ladbrokescoral.oxygen.notification.services;

import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;

public interface NotificationsMessageHandler extends MessageHandler {
  void handleSportsBookUpdate(String message);
}
