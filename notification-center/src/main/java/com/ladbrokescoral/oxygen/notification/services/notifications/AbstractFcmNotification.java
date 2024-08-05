package com.ladbrokescoral.oxygen.notification.services.notifications;

import com.google.android.gcm.server.Endpoint;
import com.google.android.gcm.server.Message;
import com.google.android.gcm.server.Sender;
import com.ladbrokescoral.oxygen.notification.entities.Device;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.services.Notifications;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public abstract class AbstractFcmNotification implements Notifications {

  /** Backward compatibility */
  private Sender legacySender;

  private Sender sender;

  private int retries;

  public AbstractFcmNotification(String serviceKey, String legacyServiceKey, int retries) {
    this.sender = new Sender(serviceKey, Endpoint.FCM);
    this.legacySender = new Sender(legacyServiceKey, Endpoint.GCM);
    this.retries = retries;
  }

  public final boolean notify(Device device, Payload payload) {
    try {
      final Message pushMessage =
          new Message.Builder()
              .addData("incident", payload.getMessage())
              .addData("_sid", "SFMC")
              .addData("alert", payload.getStatus())
              .addData("_od", payload.getDeepLink() + getEventId(payload.getEventId()))
              .addData("sound", "default")
              .addData("_m", device.getToken())
              .build();

      logger.info(
          "[RACING FLOW][WIN ALERT FLOW][FOOTBALL FLOW][ANDROID] Push notification message to send: {}",
          pushMessage.toString());

      sender.send(pushMessage, device.getToken(), retries);
      // backwards compatibility
      legacySend(pushMessage, device.getToken());
      return true;
    } catch (Exception e) {
      logger.error(
          "Error during send android GCM notification for win alert  device token  {}  {} ",
          device.toString(),
          e);
      return false;
    }
  }

  private String getEventId(Long id) {
    return id != null ? String.valueOf(id) : "";
  }

  private void legacySend(Message pushMessage, String token) {
    try {
      legacySender.send(pushMessage, token, retries);
    } catch (Exception e) {
      logger.warn("Could not send push notification with GCM server (legacy).", e);
    }
  }
}
