package com.ladbrokescoral.oxyegn.test.utils;

import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.turo.pushy.apns.ApnsClient;
import com.turo.pushy.apns.ApnsClientBuilder;
import com.turo.pushy.apns.DeliveryPriority;
import com.turo.pushy.apns.PushNotificationResponse;
import com.turo.pushy.apns.util.ApnsPayloadBuilder;
import com.turo.pushy.apns.util.SimpleApnsPushNotification;
import com.turo.pushy.apns.util.TokenUtil;
import io.netty.util.concurrent.Future;
import java.io.IOException;
import java.util.Date;
import java.util.concurrent.ExecutionException;
import org.junit.Ignore;
import org.junit.Test;

/*
 * This class is used only for testing with real IOS devices for debug
 */

public class DebugApnNotificationMessage {
  @Ignore
  @Test
  public void debugSendMsgToHeliumIos()
      throws ExecutionException, InterruptedException, IOException {
    Payload payload = Payload.builder().message("test msg").status("ok").eventId(4899933L).build();

    boolean isProduction = true; // important

    String devCertificate = "cert/helium/dev/certificate.p12";
    String prodCertificate = "cert/helium/prod/certificate.p12";

    String password = "ConnectHelium!";
    ApnsClient client =
        new ApnsClientBuilder()
            .setClientCredentials(
                getClass().getClassLoader().getResourceAsStream(prodCertificate), // important
                password)
            .setApnsServer(
                isProduction
                    ? ApnsClientBuilder.PRODUCTION_APNS_HOST
                    : ApnsClientBuilder.DEVELOPMENT_APNS_HOST)
            .build();

    String message =
        new ApnsPayloadBuilder()
            .setSoundFileName("default")
            .addCustomProperty("provider", "APNS")
            .addCustomProperty("eventId", payload.getEventId())
            .setAlertBody(
                new StringBuilder(payload.getMessage())
                    .append("\n")
                    .append(payload.getStatus())
                    .toString())
            .buildWithDefaultMaximumLength();
    String someDevToken = "27007276429235d57e5ccc6b7f95a052cd809b5faa9970b1d4ce77fee0170e8c";
    String someProdToken = "023d3de975945805650bd14212a9ee21376498c731016f4550b36c88100c3720";
    final String tokenClean = TokenUtil.sanitizeTokenString(someProdToken);

    SimpleApnsPushNotification pushNotification =
        new SimpleApnsPushNotification(
            tokenClean,
            "com.coral.GCIWhiteLabelAppRetail",
            message,
            new Date(System.currentTimeMillis() + 3600),
            DeliveryPriority.getFromCode(10));

    final Future<PushNotificationResponse<SimpleApnsPushNotification>> sendNotificationFuture =
        client.sendNotification(pushNotification);

    final PushNotificationResponse<SimpleApnsPushNotification> pushNotificationResponse =
        sendNotificationFuture.get();
    System.out.println(pushNotificationResponse);
  }
}
