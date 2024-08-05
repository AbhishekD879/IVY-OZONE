package com.ladbrokescoral.oxygen.notification.services.notifications;

import com.ladbrokescoral.oxygen.notification.entities.Device;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.services.Notifications;
import com.turo.pushy.apns.ApnsClient;
import com.turo.pushy.apns.DeliveryPriority;
import com.turo.pushy.apns.PushNotificationResponse;
import com.turo.pushy.apns.util.ApnsPayloadBuilder;
import com.turo.pushy.apns.util.SimpleApnsPushNotification;
import com.turo.pushy.apns.util.TokenUtil;
import io.netty.util.concurrent.Future;
import java.security.SecureRandom;
import java.util.Date;
import java.util.Random;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class AbstractApnNotification implements Notifications {

  /** Initial delay before first retry, without jitter (milliseconds). */
  private static final int BACKOFF_INITIAL_DELAY = 1000;

  /** Maximum delay before a retry (milliseconds). */
  private static final int MAX_BACKOFF_DELAY = 1024000;

  private final Random random = new SecureRandom();

  private ApnsClient client;
  private final String topic;
  private final int retries;

  public AbstractApnNotification(String topic, int retries, ApnsClient client) {
    this.topic = topic;
    this.retries = retries;
    this.client = client;
  }

  public final boolean notify(Device device, Payload payload) {
    try {

      final String tokenClean = TokenUtil.sanitizeTokenString(device.getToken());

      SimpleApnsPushNotification pushNotification =
          new SimpleApnsPushNotification(
              tokenClean,
              topic,
              buildMessage(payload),
              new Date(System.currentTimeMillis() + 3600),
              DeliveryPriority.getFromCode(10));

      logger.info(
          "[RACING FLOW][WIN ALERT FLOW][FOOTBALL FLOW][IOS] Push notification message to send: {}",
          pushNotification.toString());

      final Future<PushNotificationResponse<SimpleApnsPushNotification>> sendNotificationFuture =
          client.sendNotification(pushNotification);

      return attemptSend(sendNotificationFuture);

    } catch (Exception e) {
      logger.error(
          "Error during sending notification for  match alert  device token {}  {} ",
          device.toString(),
          e);
      Thread.currentThread().interrupt();
      return false;
    }
  }

  private boolean attemptSend(
      Future<PushNotificationResponse<SimpleApnsPushNotification>> sendNotificationFuture) {
    int attempt = 0;
    int backoff = BACKOFF_INITIAL_DELAY;
    do {
      attempt++;
      try {
        final PushNotificationResponse<SimpleApnsPushNotification> pushNotificationResponse =
            sendNotificationFuture.get();

        return success(pushNotificationResponse);
      } catch (final Exception e) {

        int sleepTime = backoff / 2 + random.nextInt(backoff);
        logger.warn(
            "Couldn't send notification by {} attempt. Trying again in {} milliseconds. Exception: {}",
            attempt,
            sleepTime,
            e);
        sleep(sleepTime);
        if (2 * backoff < MAX_BACKOFF_DELAY) {
          backoff *= 2;
        }
      }
    } while (attempt < retries);

    return false;
  }

  private String buildMessage(Payload payload) {
    return new ApnsPayloadBuilder()
        .setSoundFileName("default")
        .addCustomProperty("provider", "APNS")
        .addCustomProperty("eventId", payload.getEventId())
        .addCustomProperty("sportUri", payload.getDeepLink())
        .setAlertBody(payload.getMessage() + "\n" + payload.getStatus())
        .buildWithDefaultMaximumLength();
  }

  private boolean success(
      PushNotificationResponse<SimpleApnsPushNotification> pushNotificationResponse) {
    if (pushNotificationResponse.isAccepted()) {
      logger.info("Push notification accepted by APNs gateway ");
      return true;
    } else {
      logger.error(
          "Notification rejected by the APNs gateway: "
              + pushNotificationResponse.getRejectionReason());
      return false;
    }
  }

  private void sleep(long millis) {
    try {
      Thread.sleep(millis);
    } catch (InterruptedException e) {
      Thread.currentThread().interrupt();
    }
  }
}
