package com.ladbrokescoral.oxygen.notification.services.notifications;

import com.ladbrokescoral.oxygen.notification.configs.NotificationClientConfig;
import com.turo.pushy.apns.ApnsClient;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class HeliumAppleNotification extends AbstractApnNotification {
  public HeliumAppleNotification(
      @Qualifier(NotificationClientConfig.QUALIFIER_APNS_CLIENT_HELIUM) ApnsClient client,
      @Value("${helium.apple.topic}") String topic,
      @Value("${apple.retries}") int retries) {
    super(topic, retries, client);
  }
}
