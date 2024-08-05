package com.ladbrokescoral.oxygen.notification.controllers.alert;

import com.ladbrokescoral.oxygen.notification.controllers.NativeNotifications;
import org.junit.Assert;
import org.junit.Test;
import org.springframework.web.bind.WebDataBinder;

public class NativeNotificationsTest {
  @Test
  public void binderTest() {
    NativeNotifications nativeNotifications = new NativeNotifications();
    WebDataBinder webDataBinder = new WebDataBinder(Object.class);
    nativeNotifications.populateRequest(webDataBinder);
    Assert.assertNotNull(nativeNotifications);
  }
}
