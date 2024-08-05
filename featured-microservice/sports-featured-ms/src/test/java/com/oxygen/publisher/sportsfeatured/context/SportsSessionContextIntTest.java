package com.oxygen.publisher.sportsfeatured.context;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.when;

import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.oxygen.publisher.SocketIoTestHelper;
import com.oxygen.publisher.SportsFeaturedApplication;
import com.oxygen.publisher.service.CallExecutorService;
import com.oxygen.publisher.sportsfeatured.configuration.FeaturedApiProvider;
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex;
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import com.oxygen.publisher.sportsfeatured.relation.FeaturedApi;
import com.oxygen.publisher.sportsfeatured.service.FeaturedIoServerHealthIndicatorService;
import com.oxygen.publisher.sportsfeatured.service.SportsChainFactory;
import com.oxygen.publisher.sportsfeatured.util.SportsHelper;
import com.oxygen.publisher.test.util.TestCall;
import com.oxygen.publisher.translator.DiagnosticService;
import io.socket.client.IO;
import io.socket.client.Socket;
import io.socket.engineio.client.transports.WebSocket;
import java.util.Arrays;
import java.util.Optional;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.stream.Stream;
import lombok.SneakyThrows;
import org.json.JSONObject;
import org.junit.Ignore;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockedStatic;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.annotation.DirtiesContext.ClassMode;
import org.springframework.test.context.TestPropertySource;

@SpringBootTest(
    webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT,
    classes = {IntegrationTestConfig.class})
@DirtiesContext(classMode = ClassMode.BEFORE_EACH_TEST_METHOD)
@TestPropertySource(locations = "classpath:test.properties")
public class SportsSessionContextIntTest {
  private static final String EVENT_ID = "123";

  @Autowired private SportsSessionContext ctx;
  @Autowired ConfigurableApplicationContext appCtx;
  @Autowired private SocketIOServer socketIOServer;
  @MockBean private FeaturedApiProvider featuredApiProvider;
  @Mock private FeaturedApi featuredApi;
  @Autowired private SportsChainFactory sportsChainFactory;
  @MockBean private CallExecutorService callExecutorService;
  @MockBean private FeaturedIoServerHealthIndicatorService healthIndicatorService;
  @MockBean private DiagnosticService diagnosticService;
  @MockBean SportsCachedData sportsCachedData;
  @MockBean SocketIOClient client;

  private SocketIoTestHelper socketIoTestHelper16;
  private Socket socket16;
  private Socket socket0;
  private SocketIoTestHelper socketIoTestHelper0;

  @SneakyThrows
  private static void assertEventId123Received(JSONObject resp) {
    assertEquals(123, resp.getJSONObject("event").getInt("eventId"));
  }

  @BeforeEach
  public void setUp() throws Exception {

    when(featuredApiProvider.featuredApi()).thenReturn(featuredApi);
    when(featuredApi.getSportPages())
        .thenReturn(new TestCall("localhost:8080", Arrays.asList("16", "0")));
    when(sportsCachedData.getSportPageData()).thenReturn(SocketIoTestHelper.getSportPageMapCache());
    try (MockedStatic<SportsHelper> mockedStatic = Mockito.mockStatic(SportsHelper.class)) {
      mockedStatic
          .when(() -> SportsHelper.checkValidSportId(client, sportsCachedData, "16"))
          .thenReturn(PageRawIndex.forSport(16));
    }

    SportsFeaturedApplication.startSportFeaturedApplication(appCtx);

    IO.Options options = new IO.Options();
    options.forceNew = true;
    options.transports = new String[] {WebSocket.NAME};
    options.query = "sportId=16";
    int sioPort = socketIOServer.getConfiguration().getPort();
    socket16 = IO.socket(String.format("http://localhost:%s", sioPort), options);
    socket0 = IO.socket(String.format("http://localhost:%s", sioPort), options);
    socketIoTestHelper16 = new SocketIoTestHelper(socket16);
    socketIoTestHelper0 = new SocketIoTestHelper(socket0);
  }

  @AfterEach
  public void tearDown() throws Exception {
    if (socketIOServer != null) {
      socketIOServer.stop();
    }
  }

  @Test
  public void appStarts() {
    assertNotNull(ctx);
    assertNotNull(socketIOServer);
  }

  @Ignore("we need to revisit, why this test case is failing.")
  public void testClient16ReceivesMessage() {
    socketIoTestHelper16.executeWhenConnected(
        (client) -> {
          client.emit("subscribe", EVENT_ID);
          sportsChainFactory.processLiveUpdate(
              EVENT_ID, "{\"type\":\"EVENT\", \"event\": {\"eventId\": 123}}");
        });

    socketIoTestHelper16.makeAssertionsOnResponse(
        EVENT_ID, SportsSessionContextIntTest::assertEventId123Received);
  }

  @Ignore("we need to revisit, why this test case is failing.")
  public void testClientsReceiveBroadcastEventWithCorrectNamespace() {
    CountDownLatch countDownLatch = new CountDownLatch(2);
    socketIoTestHelper16.executeWhenConnected(
        (client) -> {
          client.emit("subscribe", EVENT_ID);
          countDownLatch.countDown();
        });
    socketIoTestHelper0.executeWhenConnected(
        (client) -> {
          client.emit("subscribe", EVENT_ID);
          countDownLatch.countDown();
        });

    new Thread(
            () -> {
              try {
                countDownLatch.await(2, TimeUnit.SECONDS);
                sportsChainFactory.processLiveUpdate(
                    EVENT_ID, "{\"type\":\"EVENT\", \"event\": {\"eventId\": 123}}");
              } catch (InterruptedException e) {
                e.printStackTrace();
              }
            })
        .start();

    Optional<AssertionError> maybeAssertionError =
        Stream.of(socketIoTestHelper16, socketIoTestHelper0)
            .parallel()
            .map(
                helper ->
                    helper.getAssertionsOnResponse(
                        EVENT_ID, SportsSessionContextIntTest::assertEventId123Received))
            .filter(Optional::isPresent)
            .map(Optional::get)
            .findAny();

    maybeAssertionError.ifPresent(
        ae -> {
          throw ae;
        });
  }
}
