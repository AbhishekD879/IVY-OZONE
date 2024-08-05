package com.ladbrokescoral.oxygen.notification.services.notifications;

import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.notification.entities.Device;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.entities.dto.Platform;
import com.turo.pushy.apns.ApnsClient;
import com.turo.pushy.apns.PushNotificationResponse;
import com.turo.pushy.apns.util.SimpleApnsPushNotification;
import com.turo.pushy.apns.util.concurrent.PushNotificationFuture;
import java.util.concurrent.ExecutionException;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentMatchers;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class AbstractApnNotificationTest {

  private static final int RETRIES_COUNT = 3;
  private static final String TEST_TOPIC = "com.test.topic";
  private static final String TEST_TOKEN = "sdankjdsa3i2fuejqDWEF2F329FIFME2OKFNE2UQhiuwEFNJKI2";

  @Mock private PushNotificationResponse<SimpleApnsPushNotification> notificationResponse;

  @Mock private ApnsClient client;

  @Mock
  private PushNotificationFuture<
          SimpleApnsPushNotification, PushNotificationResponse<SimpleApnsPushNotification>>
      future;

  private OxygenAppleNotification appleNotification;

  @Before
  public void setUp() throws ExecutionException, InterruptedException {
    MockitoAnnotations.initMocks(this);
    appleNotification = new OxygenAppleNotification(client, TEST_TOPIC, RETRIES_COUNT);
    when(client.sendNotification(ArgumentMatchers.any(SimpleApnsPushNotification.class)))
        .thenReturn(future);

    when(future.get())
        .thenThrow(new RuntimeException())
        .thenThrow(new RuntimeException())
        .thenReturn(notificationResponse);

    when(notificationResponse.isAccepted()).thenReturn(true);
  }

  @Test
  public void shouldSendNotificationAfterAttempts()
      throws ExecutionException, InterruptedException {
    Device device = new Device(TEST_TOKEN, Platform.IOS, null);
    Payload payload =
        Payload.builder()
            .type("type")
            .status("status")
            .message("message")
            .eventId(3122112L)
            .build();

    boolean notificationSent = appleNotification.notify(device, payload);
    verify(future, times(RETRIES_COUNT)).get();
    assertTrue(notificationSent);
  }
}
