package com.ladbrokescoral.oxygen.notification.services.notifications;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class HeliumAndroidNotification extends AbstractFcmNotification {
  public HeliumAndroidNotification(
      @Value("${helium.android.service.key}") String serviceKey,
      @Value("${helium.android.service.key.legacy}") String legacyServiceKey,
      @Value("${android.retries}") int retries) {
    super(serviceKey, legacyServiceKey, retries);
  }
}
