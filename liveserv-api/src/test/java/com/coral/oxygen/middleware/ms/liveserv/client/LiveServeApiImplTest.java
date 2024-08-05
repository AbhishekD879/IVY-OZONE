package com.coral.oxygen.middleware.ms.liveserv.client;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.mockserver.integration.ClientAndServer.startClientAndServer;

import com.coral.oxygen.middleware.ms.liveserv.client.model.SubscriptionChannel;
import com.coral.oxygen.middleware.ms.liveserv.client.model.SubscriptionRequest;
import com.coral.oxygen.middleware.ms.liveserv.client.model.SubscriptionResponse;
import com.coral.oxygen.middleware.ms.liveserv.client.model.SubscriptionStatus;
import com.coral.oxygen.middleware.ms.liveserv.model.ChannelType;
import java.util.Arrays;
import java.util.Collections;
import java.util.concurrent.TimeUnit;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.mockserver.integration.ClientAndServer;
import org.mockserver.matchers.TimeToLive;
import org.mockserver.matchers.Times;
import org.mockserver.model.HttpRequest;
import org.mockserver.model.HttpResponse;

public class LiveServeApiImplTest {

  private LiveServeApi liveServeApi;
  private ClientAndServer mockServer;

  @Before
  public void setUp() {
    this.liveServeApi = new LiveServeApiImpl("http://localhost:8080");
    mockServer = startClientAndServer(8080);
  }

  @After
  public void stopMockServer() {
    mockServer.stop();
  }

  @Test
  public void testSubscribe() {
    String response = "{\"message\": \"Response message\", " + "\"status\": \"OK\"}";

    prepareMockServerResponse(response, 200);

    SubscriptionRequest subscriptionRequest = new SubscriptionRequest();
    subscriptionRequest.setChannels(
        Collections.singletonList(new SubscriptionChannel(ChannelType.sEVENT, 100000L)));

    // when
    SubscriptionResponse subscriptionResponse = liveServeApi.subscribe(subscriptionRequest);

    // then
    assertEquals(SubscriptionStatus.OK, subscriptionResponse.getStatus());
    assertEquals("Response message", subscriptionResponse.getMessage());
  }

  @Test
  public void testSubscribeFailure() {
    String response = "{\"message\": \"Failure message\", " + "\"status\": \"FAILURE\"}";
    prepareMockServerResponse(response, 400);

    SubscriptionRequest subscriptionRequest = new SubscriptionRequest();
    subscriptionRequest.setChannels(
        Collections.singletonList(new SubscriptionChannel(ChannelType.sEVENT, 100000L)));

    // when
    SubscriptionResponse subscriptionResponse = liveServeApi.subscribe(subscriptionRequest);

    // then
    assertEquals(SubscriptionStatus.FAILURE, subscriptionResponse.getStatus());
    assertEquals(response, subscriptionResponse.getMessage());
  }

  @Test
  public void testSubscribeConnectionFailure() {

    mockServer.stopAsync();

    SubscriptionRequest subscriptionRequest = new SubscriptionRequest();
    subscriptionRequest.setChannels(
        Collections.singletonList(new SubscriptionChannel(ChannelType.sEVENT, 100000L)));

    // when
    SubscriptionResponse subscriptionResponse = liveServeApi.subscribe(subscriptionRequest);

    // then
    assertEquals(SubscriptionStatus.FAILURE, subscriptionResponse.getStatus());
    assertTrue(
        Arrays.asList("connect timed out", "Failed to connect to localhost/0:0:0:0:0:0:0:1:8080")
            .contains(subscriptionResponse.getMessage()));
  }

  private void prepareMockServerResponse(String response, int statusCode) {
    mockServer
        .when(
            HttpRequest.request().withMethod("POST").withPath("/subscription"),
            Times.unlimited(),
            TimeToLive.exactly(TimeUnit.MINUTES, 1L))
        .respond(HttpResponse.response().withStatusCode(statusCode).withBody(response));
  }
}
