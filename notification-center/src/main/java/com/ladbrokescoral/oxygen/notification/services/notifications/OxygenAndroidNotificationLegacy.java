package com.ladbrokescoral.oxygen.notification.services.notifications;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * Code changes under OZONE-1801 fire base key upgrade reading the different fire base service key
 * for diffrent app version
 */
@Component
public final class OxygenAndroidNotificationLegacy extends AbstractFcmNotification {
  public OxygenAndroidNotificationLegacy(
      @Value("${oxygen_android_service_key_old}") String serviceKey,
      @Value("${oxygen.android.service.key.legacy}") String legacyServiceKey,
      @Value("${android.retries}") int retries) {
    super(serviceKey, legacyServiceKey, retries);
  }
}
