package com.coral.oxygen.middleware.ms.liveserv.client;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertThrows;
import static org.junit.Assert.assertTrue;
import static org.mockserver.integration.ClientAndServer.startClientAndServer;

import com.coral.oxygen.middleware.ms.liveserv.exceptions.ErrorResponseException;
import java.io.IOException;
import java.time.Duration;
import java.util.concurrent.TimeUnit;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;
import org.mockserver.integration.ClientAndServer;
import org.mockserver.matchers.TimeToLive;
import org.mockserver.matchers.Times;
import org.mockserver.model.HttpRequest;
import org.mockserver.model.HttpResponse;

@RunWith(MockitoJUnitRunner.class)
public class LiveServerCallTest {

  private LiveServerCall liveServerCall;
  private ClientAndServer mockServer;

  @Before
  public void setUp() throws Exception {
    liveServerCall =
        new LiveServerCall("https://localhost:8080/push", 3, 3, 1, Duration.ofSeconds(10));
    mockServer = startClientAndServer(8080);
  }

  @After
  public void stopMockServer() {
    mockServer.stop();
  }

  @Test
  public void testSubscriptionRequest() throws Exception {
    // given
    mockServer
        .when(
            HttpRequest.request().withMethod("POST").withPath("/push"),
            Times.unlimited(),
            TimeToLive.exactly(TimeUnit.MINUTES, 1L))
        .respond(HttpResponse.response().withStatusCode(200).withBody("SomeResponse"));
    // when
    String response = liveServerCall.execute("Some Request");
    // then
    assertEquals("SomeResponse", response);
  }

  @Test
  public void testFailedSubscriptionRequest() {
    // given
    mockServer
        .when(HttpRequest.request().withMethod("POST").withPath("/push"))
        .respond(HttpResponse.response().withStatusCode(400).withBody("SomeErrorResponse"));
    // when
    ErrorResponseException thrown =
        assertThrows(
            "Expected liveServerCall.execute to throw, but it didn't",
            ErrorResponseException.class,
            () -> liveServerCall.execute("Some Request"));

    // then
    assertEquals(400, thrown.getHttpCode());
    assertEquals("SomeErrorResponse", thrown.getResponseText());
  }

  @Test
  public void testIOExceptionWhileRequest() {
    // given
    mockServer.stop();
    // when
    IOException thrown =
        assertThrows(
            "Expected liveServerCall.execute to throw IOException, but it didn't",
            IOException.class,
            () -> liveServerCall.execute("Some Request"));

    assertTrue(thrown.getMessage().contains("Failed to connect to localhost"));
  }

  @Test
  public void testICancellationAfterIOException() throws Exception {
    // given
    mockServer
        .when(
            HttpRequest.request().withMethod("POST").withPath("/push"),
            Times.unlimited(),
            TimeToLive.exactly(TimeUnit.MINUTES, 1L))
        .respond(HttpResponse.response().withStatusCode(200).withBody("SomeResponse"));
    // when
    String response = liveServerCall.execute("Some Request");
    // then
    assertEquals("SomeResponse", response);
  }
}
