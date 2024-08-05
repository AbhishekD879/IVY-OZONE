package com.oxygen.publisher.service.impl;

import static com.oxygen.publisher.inplay.context.InplaySocketMessages.*;
import static com.oxygen.publisher.server.config.SocketBuilder.IN_PLAY_SERVER_CONTEXT;
import static com.oxygen.publisher.server.config.UnitTestUtil.consumeSocketMessage;
import static com.oxygen.publisher.server.config.UnitTestUtil.fromFile;
import static com.oxygen.publisher.server.config.UnitTestUtil.getClientRooms;
import static com.oxygen.publisher.server.config.UnitTestUtil.ioServerResponseVerification;
import static com.oxygen.publisher.server.config.UnitTestUtil.listFromFile;
import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.*;
import static org.mockito.Mockito.when;

import com.corundumstudio.socketio.SocketIOServer;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.oxygen.publisher.configuration.JsonSupportConfig;
import com.oxygen.publisher.configuration.SocketIOConnectorConfiguration;
import com.oxygen.publisher.configuration.SocketIOServerConfiguration;
import com.oxygen.publisher.inplay.configuration.InplayServiceConfiguration;
import com.oxygen.publisher.inplay.context.InplayMiddlewareContext;
import com.oxygen.publisher.model.*;
import com.oxygen.publisher.server.SocketIOConnector;
import com.oxygen.publisher.server.config.SocketBuilder;
import io.socket.client.Socket;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.function.Consumer;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.json.JSONObject;
import org.junit.After;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.test.util.ReflectionTestUtils;

@Slf4j
@RunWith(MockitoJUnitRunner.class)
public class InPlaySessionContextTest {

  private static final String APP_VERSION = "85.0.0";
  private static final int SOCKET_TIMEOUT = 20;

  private SocketIOConnector socketIOConnectorService;
  private InplayCachedData cachedData;
  private Socket client;
  private Consumer<Object[]> onEmit;
  private SocketIOServer ioServer;

  @Before
  public void setUp() throws Exception {
    SocketIOConnectorConfiguration connectorConf = spy(new SocketIOConnectorConfiguration());
    InplayServiceConfiguration serviceConfiguration = spy(new InplayServiceConfiguration());
    InplayMiddlewareContext middlewareContext = mock(InplayMiddlewareContext.class);
    cachedData = spy(new InplayCachedData());
    doReturn(cachedData).when(middlewareContext).getInplayCachedData();
    //    doReturn(new InPlayData()).when(cachedData).getStructure();
    assertNull(cachedData.getSportsRibbon()); // to get rid of URF_UNREAD_FIELD findbug error
    SocketIOServerConfiguration serverConfig = new SocketIOServerConfiguration();

    JsonSupportConfig liveServeUtilsConfig = new JsonSupportConfig();

    ObjectMapper mapper = liveServeUtilsConfig.objectMapper();
    mapper.configure(SerializationFeature.FAIL_ON_EMPTY_BEANS, false);
    socketIOConnectorService =
        connectorConf.socketIOConnector(
            serverConfig.socketIOServer(
                8083,
                false,
                1,
                1,
                IN_PLAY_SERVER_CONTEXT,
                liveServeUtilsConfig.jsonSupport(mapper),
                512),
            serviceConfiguration.featuredSessionContext(APP_VERSION, middlewareContext));
    socketIOConnectorService.start();
    ioServer = (SocketIOServer) ReflectionTestUtils.getField(socketIOConnectorService, "server");
    ioServer.start();
    onEmit = mock(Consumer.class);
  }

  /**
   * Open connection response: ["version","87.0.0"] request:
   * ["subscribe","IN_PLAY_SPORTS_RIBBON_CHANGED"] no response, client joined to one room
   * "IN_PLAY_SPORTS_RIBBON_CHANGED"
   */
  @Test
  public void subscribeOnSingleTopicWithStringTest() throws Exception {
    CountDownLatch lock = ioServerResponseVerification(onEmit, APP_VERSION);
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket();
    socketBuilder.clientSocket.on(APP_VERSION_RESPONSE.messageId(), args -> onEmit.accept(args));
    client = socketBuilder.initClient();
    assertThat(lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS)).isTrue();
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    final String serverResponse = "Data for subscribed clients";
    lock = ioServerResponseVerification(onEmit, serverResponse);
    socketBuilder.clientSocket.on("EventId", args -> onEmit.accept(args));

    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    client.emit(SUBSCRIBE.messageId(), IN_PLAY_SPORTS_RIBBON_CHANGED.messageId());
    client.emit(SUBSCRIBE.messageId(), "");
    // wait some time to get time for client to join the room
    Thread.sleep(500);
    assertEquals(2, getClientRooms(ioServer, client).size());
    assertTrue(
        getClientRooms(ioServer, client).contains(IN_PLAY_SPORTS_RIBBON_CHANGED.messageId()));
    // broadcast event to all clients joined to room
    ioServer
        .getRoomOperations(IN_PLAY_SPORTS_RIBBON_CHANGED.messageId())
        .sendEvent("EventId", serverResponse);
    assertThat(lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS)).isTrue();

    client.emit(UNSUBSCRIBE.messageId(), IN_PLAY_SPORTS_RIBBON_CHANGED.messageId());
    client.emit(UNSUBSCRIBE.messageId(), "");
    // wait some time to get time for client to leave the room
    Thread.sleep(500);
    assertEquals(1, getClientRooms(ioServer, client).size());
  }

  /**
   * Open connection response: ["version","87.0.0"] request: ["subscribe",[9741103,9741798]] no
   * response, client joined to two rooms 9741103 and 9741798
   */
  @Test
  public void subscribeOnTwoTopicsWithLongTest() throws Exception {
    String EVENT_ID = "555";
    BaseObject incUpdate = new BaseObject();
    incUpdate.setType("testLiveUpdate");
    CountDownLatch lock = ioServerResponseVerification(onEmit, incUpdate);
    ConcurrentHashMap<LiveRawIndex, BaseObject> thisCache = new ConcurrentHashMap<>();
    thisCache.put(
        LiveRawIndex.builder().eventId(EVENT_ID).subjectId("t").updatedType("t").build(),
        incUpdate);
    cachedData.getLiveUpdatesCache().put(EVENT_ID, thisCache);
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket();
    client = socketBuilder.initClient();

    // verify that on subscription client receives incremental live updates for event
    socketBuilder.clientSocket.on(EVENT_ID, args -> onEmit.accept(args));
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    client.emit(SUBSCRIBE.messageId(), Arrays.asList(123L, Long.valueOf(EVENT_ID)));
    assertThat(lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS)).isTrue();
    assertEquals(3, getClientRooms(ioServer, client).size());
    assertTrue(getClientRooms(ioServer, client).contains("123"));
    assertTrue(getClientRooms(ioServer, client).contains("555"));

    client.emit(UNSUBSCRIBE.messageId(), Collections.singletonList(Long.valueOf(EVENT_ID)));
    // wait some time to get time for client to leave the room
    Thread.sleep(500);
    assertEquals(2, getClientRooms(ioServer, client).size());
  }

  @Test
  public void getVirtualRibbonTest() throws Exception {
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket();
    client = socketBuilder.initClient();
    List<VirtualSportEvents> virtualSportEventsList =
        fromFile("response/virtualSports.json", List.class);
    InPlayData inPlayData = mock(InPlayData.class);
    when(cachedData.getStructure()).thenReturn(inPlayData);
    when(inPlayData.getVirtualSportList()).thenReturn(virtualSportEventsList);
    assertSocketMessageReceived(
        GET_VIRTUAL_SPORTS_RIBBON_REQUEST.messageId(),
        GET_VIRTUAL_SPORTS_RIBBON_RESPONSE.messageId(),
        virtualSportEventsList);
  }

  @Test
  public void getRibbonTest() throws Exception {
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket();
    client = socketBuilder.initClient();

    SportsRibbon sportsRibbon = fromFile("response/get_ribbon.json", SportsRibbon.class);
    doReturn(sportsRibbon).when(cachedData).getSportsRibbon();
    assertSocketMessageReceived(
        GET_RIBBON_REQUEST.messageId(), GET_RIBBON_RESPONSE.messageId(), sportsRibbon);

    doReturn(sportsRibbon).when(cachedData).getSportsRibbonWithLiveStreams();
    assertSocketMessageReceived(
        GET_LS_RIBBON_REQUEST.messageId(), GET_LS_RIBBON_RESPONSE.messageId(), sportsRibbon);
  }

  @Ignore("response isn't received by client listener")
  @Test
  public void getInplayStructureTest() throws Exception {
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket();
    client = socketBuilder.initClient();

    InPlayData inPlayData = fromFile("response/get_inplay_structure.json", InPlayData.class);
    doReturn(inPlayData).when(cachedData).getStructureWithoutStreamEvents();
    assertSocketMessageReceived(
        GET_INPLAY_STRUCTURE_REQUEST.messageId(),
        GET_INPLAY_STRUCTURE_RESPONSE.messageId(),
        inPlayData);
  }

  private <T> void assertSocketMessageReceived(
      String socketRequestMessageId, String socketResponseMessageId, T expectedResponse)
      throws InterruptedException {
    final CountDownLatch lock1 = new CountDownLatch(1);
    client.on(socketResponseMessageId, args -> consumeSocketMessage(lock1, args, expectedResponse));
    client.emit(socketRequestMessageId);
    assertThat(lock1.await(SOCKET_TIMEOUT, TimeUnit.SECONDS)).isTrue();
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);
  }

  @Test
  @Ignore("response isn't received by client listener")
  public void onGetInplayStructureWithLiveStreamsTest() throws Exception {
    InPlayData inPlayData = fromFile("response/get_inplay_structure.json", InPlayData.class);
    doReturn(inPlayData).when(cachedData).getStructure();
    CountDownLatch lock = ioServerResponseVerification(onEmit, inPlayData);

    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket();
    socketBuilder.clientSocket.on(
        GET_INPLAY_LS_STRUCTURE_RESPONSE.messageId(), args -> onEmit.accept(args));
    client = socketBuilder.initClient();
    client.emit(GET_INPLAY_LS_STRUCTURE_REQUEST.messageId());
    assertThat(lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS)).isTrue();
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);
  }

  private void loadCacheData() {
    SportSegment expectedGetSportResponse = fromFile("response/get_sport.json", SportSegment.class);
    InPlayCache inPlayCache = fromFile("storage/InPlayCacheData.json", InPlayCache.class);
    cachedData
        .getSportSegments()
        .putAll(
            inPlayCache.getSportSegmentCaches().stream()
                .collect(
                    Collectors.toMap(
                        InPlayCache.SportSegmentCache::getStructuredKey,
                        sportSegmentCache -> sportSegmentCache)));
    inPlayCache = fromFile("storage/InPlayCacheData.json", InPlayCache.class);
    cachedData
        .getSportSegmentsWithEmptyTypes()
        .putAll(
            inPlayCache.getSportSegmentCaches().stream()
                .collect(
                    Collectors.toMap(
                        InPlayCache.SportSegmentCache::getStructuredKey,
                        sportSegmentCache -> {
                          if (sportSegmentCache.getSportSegment() != null) {
                            sportSegmentCache
                                .getSportSegment()
                                .setEventsByTypeName(
                                    sportSegmentCache
                                        .getSportSegment()
                                        .getEventsByTypeName()
                                        .stream()
                                        .map(TypeSegment::cloneWithEmptyTypes)
                                        .collect(Collectors.toList()));
                          }
                          return sportSegmentCache;
                        })));
  }

  @Test
  public void getSportTestCase() throws Exception {
    loadCacheData();
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket();
    client = socketBuilder.initClient();
    JSONObject request =
        new JSONObject(
            ("{\"categoryId\":16,\"isLiveNowType\":true,\"emptyTypes\":\"No\","
                + "\"autoUpdates\":\"Yes\",\"topLevelType\":\"LIVE_EVENT\",\"marketSelector\":\"Main Market\"}"));
    client.emit(GET_SPORT_REQUEST.messageId(), request);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    JSONObject request1 =
        new JSONObject(
            ("{\"categoryId\":171,\"isLiveNowType\":true,\"emptyTypes\":\"No\","
                + "\"autoUpdates\":\"Yes\",\"topLevelType\":\"LIVE_EVENT\",\"marketSelector\":\"Main Market,Match Betting\"}"));
    client.emit(GET_SPORT_REQUEST.messageId(), request1);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    JSONObject request2 =
        new JSONObject(
            ("{\"categoryId\":16,\"isLiveNowType\":true,\"emptyTypes\":\"Yes\","
                + "\"autoUpdates\":\"No\",\"topLevelType\":\"LIVE_EVENT\",\"marketSelector\":\"Main Market,Match Betting\"}"));
    client.emit(GET_SPORT_REQUEST.messageId(), request2);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    JSONObject request3 =
        new JSONObject(
            ("{\"categoryId\":16,\"isLiveNowType\":true,\"emptyTypes\":\"No\","
                + "\"autoUpdates\":\"No\",\"topLevelType\":\"LIVE_EVENT\",\"marketSelector\":\"Main Market\"}"));
    client.emit(GET_SPORT_REQUEST.messageId(), request3);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    JSONObject request4 =
        new JSONObject(
            ("{\"categoryId\":16,\"isLiveNowType\":true,\"emptyTypes\":\"No\","
                + "\"autoUpdates\":\"Yes\",\"topLevelType\":\"LIVE_EVENT\",\"marketSelector\":null}"));
    client.emit(GET_SPORT_REQUEST.messageId(), request4);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    JSONObject request5 =
        new JSONObject(
            ("{\"categoryId\":13,\"isLiveNowType\":true,\"emptyTypes\":\"No\","
                + "\"autoUpdates\":\"Yes\",\"topLevelType\":\"LIVE_EVENT\",\"marketSelector\":\"Main Market\"}"));
    client.emit(GET_SPORT_REQUEST.messageId(), request5);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    JSONObject request6 =
        new JSONObject(
            ("{\"categoryId\":16,\"isLiveNowType\":true,\"emptyTypes\":\"No\","
                + "\"autoUpdates\":\"Yes\",\"topLevelType\":\"LIVE_EVENT\",\"marketSelector\":\"Main Market,Match Betting\"}"));
    client.emit(GET_SPORT_REQUEST.messageId(), request6);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    JSONObject request7 =
        new JSONObject(
            ("{\"categoryId\":null,\"isLiveNowType\":true,\"emptyTypes\":\"No\","
                + "\"autoUpdates\":\"Yes\",\"topLevelType\":\"LIVE_EVENT\",\"marketSelector\":\"Main Market,Match Betting\"}"));
    client.emit(GET_SPORT_REQUEST.messageId(), request7);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    JSONObject request8 =
        new JSONObject(
            ("{\"categoryId\":16,\"isLiveNowType\":true,\"emptyTypes\":\"Yes\","
                + "\"autoUpdates\":\"Yes\",\"topLevelType\":\"LIVE_EVENT\",\"marketSelector\":\"Main Market\"}"));
    client.emit(GET_SPORT_REQUEST.messageId(), request8);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);
  }

  @Test
  public void getTypeTestCase7() throws Exception {

    List<ModuleDataItem> expectedGetTypeResponse =
        listFromFile("response/get_type.json", ModuleDataItem.class);
    InPlayCache inPlayCache = fromFile("storage/InPlayCacheData.json", InPlayCache.class);
    InplayMiddlewareContext middlewareContext = mock(InplayMiddlewareContext.class);
    inPlayCache.getSportSegmentCaches().forEach(cache -> cache.setModuleDataItem(null));

    Map<RawIndex, InPlayCache.SportSegmentCache> sportSegments =
        inPlayCache.getSportSegmentCaches().stream()
            .collect(
                Collectors.toMap(
                    InPlayCache.SportSegmentCache::getStructuredKey,
                    sportSegmentCache -> sportSegmentCache));

    cachedData.setSportSegments(sportSegments);
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket();
    client = socketBuilder.initClient();
    JSONObject request =
        new JSONObject(
            ("{\"categoryId\":16,\"isLiveNowType\":true,\"emptyTypes\":\"Yes\","
                + "\"autoUpdates\":\"No\",\"topLevelType\":\"LIVE_EVENT\", \"typeId\":442,\"marketSelector\":\"Main Market,Match Betting\"}"));
    client.emit(GET_TYPE_REQUEST.messageId(), request);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);
  }

  private void loadModuleData() {
    List<ModuleDataItem> expectedGetTypeResponse =
        listFromFile("response/get_type.json", ModuleDataItem.class);
    InPlayCache inPlayCache = fromFile("storage/InPlayCacheData.json", InPlayCache.class);
    InplayMiddlewareContext middlewareContext = mock(InplayMiddlewareContext.class);
    Map<RawIndex, InPlayCache.SportSegmentCache> sportSegments =
        inPlayCache.getSportSegmentCaches().stream()
            .collect(
                Collectors.toMap(
                    InPlayCache.SportSegmentCache::getStructuredKey,
                    sportSegmentCache -> sportSegmentCache));
    cachedData.setSportSegments(sportSegments);
  }

  @Test
  public void getTypeTestCases() throws Exception {
    loadModuleData();
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket();
    client = socketBuilder.initClient();
    JSONObject request1 =
        new JSONObject(
            ("{\"categoryId\":16,\"isLiveNowType\":true,\"emptyTypes\":\"Yes\","
                + "\"autoUpdates\":\"No\",\"topLevelType\":\"LIVE_EVENT\", \"typeId\":442,\"marketSelector\":\"Main Market\"}"));
    client.emit(GET_TYPE_REQUEST.messageId(), request1);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    JSONObject request2 =
        new JSONObject(
            ("{\"categoryId\":16,\"isLiveNowType\":true,\"emptyTypes\":\"Yes\","
                + "\"autoUpdates\":\"No\",\"topLevelType\":\"LIVE_EVENT\", \"typeId\":442,\"marketSelector\":null}"));
    client.emit(GET_TYPE_REQUEST.messageId(), request2);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    JSONObject request3 =
        new JSONObject(
            ("{\"categoryId\":16,\"isLiveNowType\":true,\"emptyTypes\":\"Yes\","
                + "\"autoUpdates\":\"No\",\"topLevelType\":\"LIVE_EVENT\", \"typeId\":443,\"marketSelector\":\"Main Market\"}"));
    client.emit(GET_TYPE_REQUEST.messageId(), request3);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    JSONObject request4 =
        new JSONObject(
            ("{\"categoryId\":16,\"isLiveNowType\":true,\"emptyTypes\":\"Yes\","
                + "\"autoUpdates\":\"No\",\"topLevelType\":\"LIVE_EVENT\", \"typeId\":442,\"marketSelector\":\"Main Market,Match Betting\"}"));
    client.emit(GET_TYPE_REQUEST.messageId(), request4);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    JSONObject request5 =
        new JSONObject(
            ("{\"categoryId\":16,\"isLiveNowType\":true,\"emptyTypes\":\"Yes\","
                + "\"autoUpdates\":\"No\",\"topLevelType\":\"LIVE_EVENT\", \"typeId\":443,\"marketSelector\":\"Main Market,Match Betting\"}"));
    client.emit(GET_TYPE_REQUEST.messageId(), request5);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);

    JSONObject request6 =
        new JSONObject(
            ("{\"categoryId\":null,\"isLiveNowType\":true,\"emptyTypes\":\"Yes\","
                + "\"autoUpdates\":\"No\",\"topLevelType\":\"LIVE_EVENT\", \"typeId\":443,\"marketSelector\":\"Main Market,Match Betting\"}"));
    client.emit(GET_TYPE_REQUEST.messageId(), request6);
    assertEquals(1, getClientRooms(ioServer, client).size());
    assertEquals("", getClientRooms(ioServer, client).toArray()[0]);
  }

  @After
  public void release() {
    if (client != null) {
      client.disconnect();
    }
    socketIOConnectorService.evict();
    ioServer.stop();
  }
}
