package com.ladbrokescoral.oxygen.notification.services.notifications;

import static com.ladbrokescoral.oxygen.notification.entities.dto.Platform.*;

import com.ladbrokescoral.oxygen.notification.entities.Device;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.services.Notifications;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class NotificationsFactory implements Notifications {

  @Autowired private OxygenAppleNotification oxygenAppleNotification;
  @Autowired private OxygenAndroidNotification oxygenAndroidNotification;
  @Autowired private OxygenAndroidNotificationLegacy oxygenAndroidNotificationLegacy;
  @Autowired private HeliumAppleNotification heliumAppleNotification;
  @Autowired private HeliumAndroidNotification heliumAndroidNotification;
  private String appVersionInt;

  public NotificationsFactory(
      OxygenAppleNotification oxygenAppleNotification,
      OxygenAndroidNotification oxygenAndroidNotification,
      OxygenAndroidNotificationLegacy oxygenAndroidNotificationLegacy,
      HeliumAppleNotification heliumAppleNotification,
      HeliumAndroidNotification HeliumAndroidNotification,
      @Value("${APP_VERSION_INT}") String appVersionInt) {
    this.oxygenAppleNotification = oxygenAppleNotification;
    this.oxygenAndroidNotification = oxygenAndroidNotification;
    this.oxygenAndroidNotificationLegacy = oxygenAndroidNotificationLegacy;
    this.heliumAppleNotification = heliumAppleNotification;
    this.heliumAndroidNotification = HeliumAndroidNotification;
    this.appVersionInt = appVersionInt;
  }

  @Override
  public boolean notify(Device device, Payload payload) {
    switch (device.getPlatform()) {
      case IOS:
        return oxygenAppleNotification.notify(device, payload);
      case ANDROID:
        return (device.getAppVersionInt() != null
                && device.getAppVersionInt() >= Integer.valueOf(appVersionInt))
            ? oxygenAndroidNotification.notify(device, payload)
            : oxygenAndroidNotificationLegacy.notify(device, payload);
      case HELIUM_IOS:
        return heliumAppleNotification.notify(device, payload);
      case HELIUM_ANDROID:
        return heliumAndroidNotification.notify(device, payload);
      default:
        logger.error("Corrupted payload for notification, unknown type of provider");
        return false;
    }
  }
}
