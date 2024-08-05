package com.ladbrokescoral.oxygen.notification.services.notifications;

import com.ladbrokescoral.oxygen.notification.configs.NotificationClientConfig;
import com.turo.pushy.apns.ApnsClient;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class OxygenAppleNotification extends AbstractApnNotification {

  public OxygenAppleNotification(
      @Qualifier(NotificationClientConfig.QUALIFIER_APNS_CLIENT_OXYGEN) ApnsClient client,
      @Value("${oxygen.apple.topic}") String topic,
      @Value("${apple.retries}") int retries) {

    super(topic, retries, client);
  }
}
