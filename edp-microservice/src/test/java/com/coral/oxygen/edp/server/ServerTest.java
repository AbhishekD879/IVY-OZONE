package com.coral.oxygen.edp.server;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;
import static org.mockito.ArgumentMatchers.any;

import com.coral.oxygen.edp.liveserv.LiveServConnector;
import com.coral.oxygen.edp.liveserv.LiveServMessageConverter;
import com.coral.oxygen.edp.model.output.OutputEvent;
import com.coral.oxygen.edp.model.output.OutputMarket;
import com.coral.oxygen.edp.model.output.OutputOutcome;
import com.coral.oxygen.edp.tracking.Subscription;
import com.coral.oxygen.edp.tracking.Tracker;
import com.coral.oxygen.edp.tracking.model.CategoryToUpcomingEvent;
import com.coral.oxygen.edp.tracking.model.EventData;
import com.coral.oxygen.edp.tracking.model.FirstMarketsData;
import com.corundumstudio.socketio.AckMode;
import com.corundumstudio.socketio.SocketConfig;
import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.Transport;
import com.corundumstudio.socketio.protocol.JacksonJsonSupport;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.socket.client.IO;
import io.socket.client.IO.Options;
import io.socket.client.Socket;
import java.net.URI;
import java.util.Collections;
import java.util.List;
import java.util.function.Consumer;
import org.json.JSONException;
import org.json.JSONObject;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.skyscreamer.jsonassert.JSONAssert;

// FIXME: need rework. optimise elapsed run-time for tests
// 1) no need to start server for each test
// 2) use SpringBoot test
@ExtendWith(MockitoExtension.class)
public class ServerTest {

  private static final int TEST_PORT = 8585;
  private static final long TIMEOUT = 10000;

  @Mock private Tracker<Long, FirstMarketsData> trackerMock;
  @Mock private Tracker<Long, EventData> virtualMarketsTrackerMock;
  @Mock private LiveServConnector lsConnectorMock;
  @Mock private LiveServMessageConverter lsConverterMock;
  @Mock private Consumer<Object> consumerMock;
  @Mock private Tracker<String, List<CategoryToUpcomingEvent>> sportsTrackerMock;

  private Server server;
  private Socket client;

  private ObjectMapper objectMapper = new ObjectMapper();

  @BeforeEach
  public void setUp() throws Exception {

    server =
        new Server(
            ServerTest.socketIOServer(TEST_PORT),
            trackerMock,
            virtualMarketsTrackerMock,
            lsConnectorMock,
            lsConverterMock,
            sportsTrackerMock);
    server.start();

    URI uri = new URI("http://localhost:" + TEST_PORT);

    IO.Options options = prepareSocketConfigurations("/edp");
    client = IO.socket(uri, options);
    client.on(Server.EVENT_DATA_RESPONSE, args -> consumerMock.accept(args[0]));
    client.connect();
    while (!client.connected()) {
      Thread.sleep(50);
    }
  }

  @AfterEach
  public void tearDown() {
    server.stop();
  }

  @Test
  public void testSubscribe() {
    client.emit(Server.SUBSCRIBE_FIRST_5_MARKETS, 10L);
    ArgumentCaptor<Subscription> subscriptionCaptor = ArgumentCaptor.forClass(Subscription.class);
    Mockito.verify(trackerMock, Mockito.timeout(TIMEOUT))
        .addSubscription(subscriptionCaptor.capture());
    Subscription subscription = subscriptionCaptor.getValue();

    assertEquals(client.id(), subscription.getClientId());
    assertEquals(10L, subscription.getTicket());
  }

  @Test
  public void testUnsubscribe() {
    client.emit(Server.SUBSCRIBE_FIRST_5_MARKETS, 10L);
    client.emit(Server.UNSUBSCRIBE_ALL_MARKETS, 10L);

    Mockito.verify(trackerMock, Mockito.timeout(TIMEOUT)).removeSubscription(client.id(), 10L);
  }

  @Test
  public void testUnsubscribeWithEmpty() {
    client.emit(Server.SUBSCRIBE_FIRST_5_MARKETS, 10L);
    try {
      client.emit(Server.UNSUBSCRIBE_ALL_MARKETS, "");
    } catch (Exception e) {
      fail("No exception should be trigger on empty unsubscribe");
    }
  }

  @Test
  public void testDisconnect() {
    client.emit(Server.SUBSCRIBE_FIRST_5_MARKETS, 10L);
    Mockito.verify(trackerMock, Mockito.timeout(TIMEOUT)).addSubscription(any());
    client.disconnect();

    Mockito.verify(trackerMock, Mockito.timeout(TIMEOUT)).removeSubscription(client.id(), 10L);
  }

  @Test
  public void testReceiveMessage() throws JsonProcessingException, JSONException {
    client.emit(Server.SUBSCRIBE_FIRST_5_MARKETS, 10L);
    ArgumentCaptor<Subscription> subscriptionCaptor = ArgumentCaptor.forClass(Subscription.class);
    Mockito.verify(trackerMock, Mockito.timeout(TIMEOUT))
        .addSubscription(subscriptionCaptor.capture());
    Subscription<Long, FirstMarketsData> subscription = subscriptionCaptor.getValue();

    FirstMarketsData data = new FirstMarketsData();
    OutputEvent event = new OutputEvent();
    event.setId(10L);
    event.setMarketsCount(1);
    data.setEvent(event);
    OutputMarket market = new OutputMarket();
    market.setId("110");
    data.getEvent().setMarkets(Collections.singletonList(market));
    OutputOutcome outcome = new OutputOutcome();
    outcome.setId("1110");
    data.getEvent().getMarkets().get(0).setOutcomes(Collections.singletonList(outcome));
    subscription.emit(data);

    String expectedData = objectMapper.writeValueAsString(data);

    ArgumentCaptor<JSONObject> responseCaptor = ArgumentCaptor.forClass(JSONObject.class);
    Mockito.verify(consumerMock, Mockito.timeout(TIMEOUT)).accept(responseCaptor.capture());
    JSONObject actualData = responseCaptor.getValue();
    JSONAssert.assertEquals(expectedData, actualData, false);
  }

  @Test
  public void testReceiveMessageMarketWithEachWayAvailable()
      throws JsonProcessingException, JSONException {
    client.emit(Server.SUBSCRIBE_VIRTUAL_MARKETS, 10L);
    ArgumentCaptor<Subscription> subscriptionCaptor = ArgumentCaptor.forClass(Subscription.class);
    Mockito.verify(virtualMarketsTrackerMock, Mockito.timeout(TIMEOUT))
        .addSubscription(subscriptionCaptor.capture());
    Subscription<Long, FirstMarketsData> subscription = subscriptionCaptor.getValue();

    FirstMarketsData data = new FirstMarketsData();
    OutputEvent event = new OutputEvent();
    event.setId(10L);
    event.setMarketsCount(1);
    data.setEvent(event);
    OutputMarket market = new OutputMarket();
    market.setId("110");
    market.setIsEachWayAvailable(true);
    data.getEvent().setMarkets(Collections.singletonList(market));
    OutputOutcome outcome = new OutputOutcome();
    outcome.setId("1110");
    data.getEvent().getMarkets().get(0).setOutcomes(Collections.singletonList(outcome));
    subscription.emit(data);

    String expectedData = objectMapper.writeValueAsString(data);

    ArgumentCaptor<JSONObject> responseCaptor = ArgumentCaptor.forClass(JSONObject.class);
    Mockito.verify(consumerMock, Mockito.timeout(TIMEOUT)).accept(responseCaptor.capture());
    JSONObject actualData = responseCaptor.getValue();
    JSONAssert.assertEquals(expectedData, actualData, false);
    assertTrue(actualData.toString().contains("isEachWayAvailable"));
  }

  @Test
  public void testReceiveMessageAndUnsubscribe() {
    client.emit(Server.SUBSCRIBE_FIRST_5_MARKETS, 10L);
    ArgumentCaptor<Subscription> subscriptionCaptor = ArgumentCaptor.forClass(Subscription.class);
    Mockito.verify(trackerMock, Mockito.timeout(TIMEOUT))
        .addSubscription(subscriptionCaptor.capture());
    Subscription<Long, FirstMarketsData> subscription = subscriptionCaptor.getValue();

    FirstMarketsData data = new FirstMarketsData();
    OutputEvent event = new OutputEvent();
    event.setId(10L);
    event.setMarketsCount(1);
    data.setEvent(event);
    OutputMarket market = new OutputMarket();
    market.setId("110");
    data.getEvent().setMarkets(Collections.singletonList(market));
    OutputOutcome outcome = new OutputOutcome();
    outcome.setId("1110");
    data.getEvent().getMarkets().get(0).setOutcomes(Collections.singletonList(outcome));
    subscription.emit(data);

    client.emit(Server.UNSUBSCRIBE_ALL_MARKETS, 10L);
    Mockito.verify(trackerMock, Mockito.timeout(TIMEOUT)).removeSubscription(client.id(), 10L);
  }

  private static SocketIOServer socketIOServer(int port) {
    com.corundumstudio.socketio.Configuration configuration =
        new com.corundumstudio.socketio.Configuration();
    configuration.setContext("/edp");
    configuration.setPort(port);
    configuration.setAckMode(AckMode.AUTO);
    configuration.setTransports(Transport.WEBSOCKET, Transport.POLLING);
    SocketConfig socketConfig = new SocketConfig();
    socketConfig.setReuseAddress(true);
    configuration.setSocketConfig(socketConfig);
    configuration.setJsonSupport(new JacksonJsonSupport());
    return new SocketIOServer(configuration);
  }

  private static Options prepareSocketConfigurations(String path) {
    Options options = new Options();

    options.path = path;
    options.query = "{}";
    options.upgrade = false;
    options.reconnectionDelay = 1000;
    options.forceNew = true;
    options.timeout = 5000;
    options.reconnectionAttempts = 100;

    return options;
  }
}
