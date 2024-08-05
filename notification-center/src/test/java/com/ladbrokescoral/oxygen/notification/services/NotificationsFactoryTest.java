package com.ladbrokescoral.oxygen.notification.services;

import com.ladbrokescoral.oxygen.notification.entities.Device;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.entities.dto.Platform;
import com.ladbrokescoral.oxygen.notification.services.notifications.*;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
public class NotificationsFactoryTest {

  @InjectMocks private NotificationsFactory Factory;

  @Value("${oxygen.android.service.key}")
  private String serviceKey;

  @Value("${oxygen.android.service.key.old}")
  private String serviceKeylgacy;

  @Value("${oxygen.android.service.key.legacy}")
  private String legacyServiceKey;

  @Mock private OxygenAppleNotification oxygenAppleNotification;
  private OxygenAndroidNotification oxygenAndroidNotification;
  private OxygenAndroidNotificationLegacy oxygenAndroidNotificationLegacy;
  @Mock private HeliumAppleNotification heliumAppleNotification;
  @Mock private HeliumAndroidNotification heliumAndroidNotification;

  @Before
  public void setUp() throws NoSuchFieldException, IllegalAccessException {

    oxygenAndroidNotification = new OxygenAndroidNotification(serviceKey, legacyServiceKey, 1);
    oxygenAndroidNotificationLegacy =
        new OxygenAndroidNotificationLegacy(serviceKeylgacy, legacyServiceKey, 1);
    Factory =
        new NotificationsFactory(
            oxygenAppleNotification,
            oxygenAndroidNotification,
            oxygenAndroidNotificationLegacy,
            heliumAppleNotification,
            heliumAndroidNotification,
            "60700");
  }

  @Test
  public void NotificationsFactoryTestInvalidRequest() {

    Assert.assertEquals(
        false,
        Factory.notify(
            new Device("test", Platform.ANDROID, null),
            Payload.builder()
                .message("test")
                .status("TEST")
                .deepLink("test")
                .type("winalert")
                .build()));
  }

  @Test
  public void NotificationsFactoryNewKeyTestInvalidRequest() {

    Assert.assertEquals(
        false,
        Factory.notify(
            new Device("test", Platform.ANDROID, 60700),
            Payload.builder()
                .message("test")
                .status("TEST")
                .deepLink("test")
                .type("winalert")
                .build()));
  }

  @Test
  public void NotificationsFactoryNewKeyTestInvalidRequests() {

    Assert.assertEquals(
        false,
        Factory.notify(
            new Device("test", Platform.ANDROID, 60000),
            Payload.builder()
                .message("test")
                .status("TEST")
                .deepLink("test")
                .type("winalert")
                .build()));
  }

  @Test
  public void NotificationsFactoryHeliumIosTestInvalidRequests() {

    Assert.assertEquals(
        false,
        Factory.notify(
            new Device("test", Platform.HELIUM_IOS, 60000),
            Payload.builder()
                .message("test")
                .status("TEST")
                .deepLink("test")
                .type("winalert")
                .build()));
  }

  @Test
  public void NotificationsFactoryIosTestInvalidRequests() {

    Assert.assertEquals(
        false,
        Factory.notify(
            new Device("test", Platform.IOS, 60000),
            Payload.builder()
                .message("test")
                .status("TEST")
                .deepLink("test")
                .type("winalert")
                .build()));
  }
}
