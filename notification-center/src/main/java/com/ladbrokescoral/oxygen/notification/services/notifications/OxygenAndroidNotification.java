package com.ladbrokescoral.oxygen.notification.services.notifications;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public final class OxygenAndroidNotification extends AbstractFcmNotification {
  public OxygenAndroidNotification(
      @Value("${oxygen_android_service_key}") String serviceKey,
      @Value("${oxygen.android.service.key.legacy}") String legacyServiceKey,
      @Value("${android.retries}") int retries) {
    super(serviceKey, legacyServiceKey, retries);
  }
}
