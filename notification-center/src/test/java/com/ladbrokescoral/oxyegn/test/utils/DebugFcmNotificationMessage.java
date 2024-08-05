package com.ladbrokescoral.oxyegn.test.utils;

import com.ladbrokescoral.oxygen.notification.entities.Device;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.entities.dto.Platform;
import com.ladbrokescoral.oxygen.notification.services.notifications.AbstractFcmNotification;
import com.ladbrokescoral.oxygen.notification.services.notifications.HeliumAndroidNotification;
import org.junit.Ignore;
import org.junit.Test;

/*
 * This class is used only for testing with real Android devices for debug
 */
public class DebugFcmNotificationMessage {
  @Ignore
  @Test
  public void debugSendMsgToHelium() {
    AbstractFcmNotification fcmNotification =
        new HeliumAndroidNotification(
            "AIzaSyBJZG4TE2F9I00JcLnqFUex1JscxEvE0WU",
            "AIzaSyBJZG4TE2F9I00JcLnqFUex1JscxEvE0WU",
            3);
    Device helium_android =
        new Device(
            "dGRjMLt95rw:APA91bEORaicCKlDYyq39DrI0_8GvLx6jaPfAPFwmbYDP9Ft9GFCvB7u-RapKf57zb0hezv4OurhytFXv0fl5KfRRt80vDRKDlC3Ur4z2N3ooora5e7q4AS3JmdId6JzjJ2XyoQ0-SOD",
            Platform.HELIUM_ANDROID,
            null);
    Payload payload = Payload.builder().message("").status("ok").eventId(231213213L).build();
    fcmNotification.notify(helium_android, payload);
  }
}
