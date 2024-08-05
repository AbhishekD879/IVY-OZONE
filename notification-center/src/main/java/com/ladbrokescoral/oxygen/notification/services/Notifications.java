package com.ladbrokescoral.oxygen.notification.services;

import com.ladbrokescoral.oxygen.notification.entities.Device;
import com.ladbrokescoral.oxygen.notification.entities.Payload;

public interface Notifications {
  boolean notify(Device device, Payload payload);
}
