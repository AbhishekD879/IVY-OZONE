package com.oxygen.publisher.service.impl

import com.corundumstudio.socketio.SocketIOServer
import com.fasterxml.jackson.databind.ObjectMapper
import com.oxygen.publisher.configuration.JsonSupportConfig
import com.oxygen.publisher.configuration.SocketIOConnectorConfiguration
import com.oxygen.publisher.configuration.SocketIOServerConfiguration
import com.oxygen.publisher.inplay.configuration.InplayServiceConfiguration
import com.oxygen.publisher.inplay.context.InplayMiddlewareContext
import com.oxygen.publisher.inplay.context.InplaySessionContext
import com.oxygen.publisher.model.*
import com.oxygen.publisher.server.SocketIOConnector
import com.oxygen.publisher.server.config.SocketBuilder
import io.socket.client.Socket
import org.json.JSONObject
import org.skyscreamer.jsonassert.JSONAssert
import org.springframework.test.util.ReflectionTestUtils
import spock.lang.Ignore
import spock.lang.Specification

import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import java.util.function.Consumer
import java.util.stream.Collectors

import static com.oxygen.publisher.server.config.UnitTestUtil.fromFile
import static com.oxygen.publisher.server.config.UnitTestUtil.getClientRooms

import static com.oxygen.publisher.inplay.context.InplaySocketMessages.APP_VERSION_RESPONSE;
import static com.oxygen.publisher.inplay.context.InplaySocketMessages.GET_INPLAY_LS_STRUCTURE_REQUEST;
import static com.oxygen.publisher.inplay.context.InplaySocketMessages.GET_INPLAY_LS_STRUCTURE_RESPONSE
import static com.oxygen.publisher.inplay.context.InplaySocketMessages.GET_LS_RIBBON_REQUEST;
import static com.oxygen.publisher.inplay.context.InplaySocketMessages.GET_LS_RIBBON_RESPONSE;
import static com.oxygen.publisher.inplay.context.InplaySocketMessages.GET_RIBBON_REQUEST;
import static com.oxygen.publisher.inplay.context.InplaySocketMessages.GET_RIBBON_RESPONSE;
import static com.oxygen.publisher.inplay.context.InplaySocketMessages.GET_SPORT_REQUEST
import static com.oxygen.publisher.inplay.context.InplaySocketMessages.GET_TYPE_REQUEST
import static com.oxygen.publisher.inplay.context.InplaySocketMessages.SUBSCRIBE;
import static com.oxygen.publisher.inplay.context.InplaySocketMessages.UNSUBSCRIBE
import static com.oxygen.publisher.server.config.UnitTestUtil.listFromFile;

@Ignore
class InPlaySessionContextSpec extends Specification {
  SocketIOConnector socketIOConnectorService
  InplaySessionContext sessionContext

  InplayMiddlewareContext middlewareContext

  InplayCachedData cachedData
  Socket client

  Consumer<Object[]> onEmit
  SocketIOServer ioServer

  String appVersion = "85.0.0"
  static final int SOCKET_TIMEOUT = 10
  static final String IN_PLAY_SERVER_CONTEXT = "/websocket"

  JsonSupportConfig liveServeUtilsConfig = new JsonSupportConfig()
  private ObjectMapper objectMapper = liveServeUtilsConfig.objectMapper()

  def setup() throws Exception {
    // prepare some inplay middleware context to pass to socket.io connector
    cachedData = Spy(new InplayCachedData())
    cachedData.getStructure() >> new InPlayData()
    assert cachedData.getSportsRibbon() == null// to get rid of URF_UNREAD_FIELD findbug error

    middlewareContext = Mock(InplayMiddlewareContext)
    middlewareContext.getInplayCachedData() >> cachedData

    onEmit = Mock(Consumer)

    // create socketio server configuration and session context
    SocketIOServerConfiguration serverConfig = new SocketIOServerConfiguration()
    sessionContext = new InplayServiceConfiguration().featuredSessionContext(appVersion, middlewareContext)

    // create and start service (connector), that is working with socket.io
    socketIOConnectorService = new SocketIOConnectorConfiguration().socketIOConnector(
        serverConfig.socketIOServer(8083, false, 1000, 100,
        IN_PLAY_SERVER_CONTEXT, liveServeUtilsConfig.jsonSupport(objectMapper)),
        sessionContext)
    socketIOConnectorService.start()

    // start socket.io server
    ioServer = (SocketIOServer) ReflectionTestUtils.getField(socketIOConnectorService, "server")
    ioServer.start()
  }

  private CountDownLatch ioServerResponseVerification(Consumer<Object[]> onEmit, String expectedResponse) {
    CountDownLatch lock = new CountDownLatch(1);

    onEmit.accept(_) >> { arguments ->
      // server response
      Object[] msg = arguments[0]
      println "\n\n\n\n" + msg[0]
      println expectedResponse
      assert msg.length > 0
      assert msg[0] == expectedResponse
      lock.countDown()

      return msg;
    }

    return lock;
  }

  private CountDownLatch ioServerResponseVerification(Consumer<Object[]> onEmit, Object expectedResponse) {
    CountDownLatch lock = new CountDownLatch(1);

    onEmit.accept(_) >> { arguments ->
      // server response
      Object[] msg = arguments[0]
      println "\n\n\n\n" + msg[0]
      def expectedJson = objectMapper.writeValueAsString(expectedResponse)
      println expectedJson
      assert msg.length > 0
      JSONAssert.assertEquals(expectedJson, String.valueOf(msg[0]), true)
      lock.countDown()

      return msg
    }

    return lock;
  }

  /**
   * Open connection
   * response: ["version","87.0.0"]
   * request: ["subscribe","IN_PLAY_SPORTS_RIBBON_CHANGED"]
   * no response, client joined to one room "IN_PLAY_SPORTS_RIBBON_CHANGED"
   */
  def "After initClient and 1 listener - check existing rooms"() throws Exception {
    CountDownLatch lock = ioServerResponseVerification(onEmit, appVersion)
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket()

    when:
    socketBuilder.clientSocket.on(APP_VERSION_RESPONSE.messageId(), { args -> onEmit.accept(args) })
    client = socketBuilder.initClient()

    then:
    lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS) == true
    1 == getClientRooms(ioServer, client).size()
    "" == getClientRooms(ioServer, client).toArray()[0]
  }

  def "After initClient and 2 listeners - check existing rooms"() throws Exception {
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket()

    when:
    socketBuilder.clientSocket.on(APP_VERSION_RESPONSE.messageId(), { args -> onEmit.accept(args) })
    client = socketBuilder.initClient()
    CountDownLatch lock = ioServerResponseVerification(onEmit, "Data for subscribed clients")
    socketBuilder.clientSocket.on("EventId", { args -> onEmit.accept(args) })

    then:
    1 == getClientRooms(ioServer, client).size()
    "" == getClientRooms(ioServer, client).toArray()[0]
  }

  def "After initClient and 2 listeners and subscribe twice - check existing rooms"() throws Exception {
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket()

    when:
    socketBuilder.clientSocket.on(APP_VERSION_RESPONSE.messageId(), { args -> onEmit.accept(args) })
    client = socketBuilder.initClient()
    CountDownLatch lock = ioServerResponseVerification(onEmit, "Data for subscribed clients")
    socketBuilder.clientSocket.on("EventId", { args -> onEmit.accept(args) })
    client.emit(SUBSCRIBE.messageId(), IN_PLAY_SPORTS_RIBBON_CHANGED.messageId())
    client.emit(SUBSCRIBE.messageId(), "")
    // wait some time to get time for client to join the room
    Thread.sleep(500)

    then:
    2 == getClientRooms(ioServer, client).size()
    getClientRooms(ioServer, client).contains(IN_PLAY_SPORTS_RIBBON_CHANGED.messageId())
  }

  def "After initClient and 2 listeners and subscribe twice and server emit event  - check lock await"() throws Exception {
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket()
    socketBuilder.clientSocket.on(APP_VERSION_RESPONSE.messageId(), { args -> onEmit.accept(args) })

    when:
    client = socketBuilder.initClient()
    final String serverResponse = "Data for subscribed clients"
    CountDownLatch lock = ioServerResponseVerification(onEmit, serverResponse)
    socketBuilder.clientSocket.on("EventId", { args -> onEmit.accept(args) })
    client.emit(SUBSCRIBE.messageId(), IN_PLAY_SPORTS_RIBBON_CHANGED.messageId())
    client.emit(SUBSCRIBE.messageId(), "")
    Thread.sleep(500)
    // broadcast event to all clients joined to room
    ioServer.getRoomOperations(IN_PLAY_SPORTS_RIBBON_CHANGED.messageId()).sendEvent("EventId", serverResponse)

    then:
    lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS)
  }

  def "After subscribe twice, then twice unsubscribe - rooms amount = 1"() throws Exception {
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket()
    socketBuilder.clientSocket.on(APP_VERSION_RESPONSE.messageId(), { args -> onEmit.accept(args) })

    when:
    client = socketBuilder.initClient()
    final String serverResponse = "Data for subscribed clients"
    CountDownLatch lock = ioServerResponseVerification(onEmit, serverResponse)
    socketBuilder.clientSocket.on("EventId", { args -> onEmit.accept(args) })
    client.emit(SUBSCRIBE.messageId(), IN_PLAY_SPORTS_RIBBON_CHANGED.messageId())
    client.emit(SUBSCRIBE.messageId(), "")
    Thread.sleep(500)

    ioServer.getRoomOperations(IN_PLAY_SPORTS_RIBBON_CHANGED.messageId()).sendEvent("EventId", serverResponse)
    client.emit(UNSUBSCRIBE.messageId(), IN_PLAY_SPORTS_RIBBON_CHANGED.messageId())
    client.emit(UNSUBSCRIBE.messageId(), "")
    // wait some time to get time for client to leave the room
    Thread.sleep(500)

    then:
    1 == getClientRooms(ioServer, client).size()
  }

  /**
   * Open connection
   * response: ["version","87.0.0"]
   * request: ["subscribe",[9741103,9741798]]
   * no response, client joined to two rooms 9741103 and 9741798
   */
  def subscribeOnTwoTopicsWithLongTest() throws Exception {
    String EVENT_ID = "555"
    BaseObject incUpdate = new BaseObject()
    incUpdate.setType("testLiveUpdate")
    CountDownLatch lock = ioServerResponseVerification(onEmit, incUpdate)
    ConcurrentHashMap<LiveRawIndex, BaseObject> thisCache = new ConcurrentHashMap<>()
    thisCache.put(new LiveRawIndex(EVENT_ID, "t", "t"), incUpdate)
    cachedData.getLiveUpdatesCache().put(EVENT_ID, thisCache)
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket()
    client = socketBuilder.initClient()
    when:
    socketBuilder.clientSocket.on(EVENT_ID, { args -> onEmit.accept(args) })
    then:
    1 == getClientRooms(ioServer, client).size()
    "" == getClientRooms(ioServer, client).toArray()[0]
  }

  def subscribeOnTwoTopicsWithLongTest2() throws Exception {
    String EVENT_ID = "555"
    BaseObject incUpdate = new BaseObject()
    incUpdate.setType("testLiveUpdate")
    CountDownLatch lock = ioServerResponseVerification(onEmit, incUpdate)
    ConcurrentHashMap<LiveRawIndex, BaseObject> thisCache = new ConcurrentHashMap<>()
    thisCache.put(new LiveRawIndex(EVENT_ID, "t", "t"), incUpdate)
    cachedData.getLiveUpdatesCache().put(EVENT_ID, thisCache)
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket()
    client = socketBuilder.initClient()
    when:
    socketBuilder.clientSocket.on(EVENT_ID, { args -> onEmit.accept(args) })
    client.emit(SUBSCRIBE.messageId(), Arrays.asList(123L, Long.valueOf(EVENT_ID)))

    then:
    lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS)
    3 == getClientRooms(ioServer, client).size()
    getClientRooms(ioServer, client).contains("123")
    getClientRooms(ioServer, client).contains("555")
  }

  def subscribeOnTwoTopicsWithLongTest3() throws Exception {
    String EVENT_ID = "555"
    BaseObject incUpdate = new BaseObject()
    incUpdate.setType("testLiveUpdate")
    CountDownLatch lock = ioServerResponseVerification(onEmit, incUpdate)
    ConcurrentHashMap<LiveRawIndex, BaseObject> thisCache = new ConcurrentHashMap<>()
    thisCache.put(new LiveRawIndex(EVENT_ID, "t", "t"), incUpdate)
    cachedData.getLiveUpdatesCache().put(EVENT_ID, thisCache)
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket()
    client = socketBuilder.initClient()

    when:
    socketBuilder.clientSocket.on(EVENT_ID, { args -> onEmit.accept(args) })
    client.emit(SUBSCRIBE.messageId(), Arrays.asList(123L, Long.valueOf(EVENT_ID)))
    client.emit(UNSUBSCRIBE.messageId(), Collections.singletonList(Long.valueOf(EVENT_ID)))
    // wait some time to get time for client to leave the room
    Thread.sleep(500)

    then:
    2 == getClientRooms(ioServer, client).size()
  }

  def getRibbonTest() throws Exception {
    SportsRibbon sportsRibbon = fromFile("response/get_ribbon.json", SportsRibbon.class)
    cachedData.getSportsRibbon() >> sportsRibbon
    CountDownLatch lock = ioServerResponseVerification(onEmit, sportsRibbon)

    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket()
    socketBuilder.clientSocket.on(GET_RIBBON_RESPONSE.messageId(), { args -> onEmit.accept(args) })

    when:
    client = socketBuilder.initClient()
    client.emit(GET_RIBBON_REQUEST.messageId())

    then:
    lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS)
    1 == getClientRooms(ioServer, client).size()
    "" == getClientRooms(ioServer, client).toArray()[0]
  }

  def getRibbonTest2() throws Exception {
    SportsRibbon sportsRibbon = fromFile("response/get_ribbon.json", SportsRibbon.class)
    cachedData.getSportsRibbon() >> sportsRibbon
    CountDownLatch lock = ioServerResponseVerification(onEmit, sportsRibbon)

    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket()
    socketBuilder.clientSocket.on(GET_RIBBON_RESPONSE.messageId(), { args -> onEmit.accept(args) })

    when:
    client = socketBuilder.initClient()
    client.emit(GET_RIBBON_REQUEST.messageId())

    cachedData.getSportsRibbonWithLiveStreams() >> sportsRibbon
    socketBuilder.clientSocket.on(GET_LS_RIBBON_RESPONSE.messageId(), { args -> onEmit.accept(args) })
    client.emit(GET_LS_RIBBON_REQUEST.messageId())

    then:
    lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS)
    1 == getClientRooms(ioServer, client).size()
    "" == getClientRooms(ioServer, client).toArray()[0]
  }

  // TODO - Not working - fix
  //    def getInplayStructureTest() throws Exception {
  //        InPlayData inPlayData = fromFile("response/get_inplay_structure.json", InPlayData.class)
  //        cachedData.getStructure() >> inPlayData
  //        CountDownLatch lock = ioServerResponseVerification(onEmit, inPlayData)
  //
  //        SocketBuilder socketBuilder = SocketBuilder.getInplaySocket()
  //        socketBuilder.clientSocket.on(GET_INPLAY_STRUCTURE_RESPONSE.messageId(), { args -> onEmit.accept(args) })
  //        client = socketBuilder.initClient()
  //
  //        when:
  //        client.emit(GET_INPLAY_STRUCTURE_REQUEST.messageId())
  //
  //        then:
  //        lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS)
  //        1 == getClientRooms(ioServer, client).size()
  //        "" == getClientRooms(ioServer, client).toArray()[0]
  //    }

  def onGetInplayStructureWithLiveStreamsTest() throws Exception {
    InPlayData inPlayData = fromFile("response/get_inplay_structure.json", InPlayData.class)
    cachedData.getStructureWithoutUpcomingEvents() >> inPlayData
    CountDownLatch lock = ioServerResponseVerification(onEmit, inPlayData)

    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket()
    socketBuilder.clientSocket.on(GET_INPLAY_LS_STRUCTURE_RESPONSE.messageId(), { args -> onEmit.accept(args) })
    client = socketBuilder.initClient()

    when:
    client.emit(GET_INPLAY_LS_STRUCTURE_REQUEST.messageId())

    then:
    lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS)
    1 == getClientRooms(ioServer, client).size()
    "" == getClientRooms(ioServer, client).toArray()[0]
  }

  def getSportTest() throws Exception {
    SportSegment expectedGetSportResponse = fromFile("response/get_sport.json", SportSegment.class)
    InPlayCache inPlayCache = fromFile("storage/InPlayCache.json", InPlayCache.class)
    cachedData.getSportSegments().putAll(inPlayCache.getSportSegmentCaches()
        .stream()
        .collect(Collectors.toMap({ sportSegmentCache -> sportSegmentCache.getStructuredKey() },
        { sportSegmentCache -> sportSegmentCache })))
    inPlayCache = fromFile("storage/InPlayCache.json", InPlayCache.class)
    cachedData.getSportSegmentsWithEmptyTypes().putAll(inPlayCache.getSportSegmentCaches()
        .stream()
        .collect(Collectors.toMap({ sportSegmentCache -> sportSegmentCache.getStructuredKey() }, { sportSegmentCache ->
          if (sportSegmentCache.getSportSegment() != null) {
            sportSegmentCache.getSportSegment()
                .setEventsByTypeName(sportSegmentCache.getSportSegment().getEventsByTypeName()
                .stream().map({ typeSegment -> typeSegment.cloneWithEmptyTypes() }).collect(Collectors.toList()))
          }
          return sportSegmentCache
        })))
    CountDownLatch lock = ioServerResponseVerification(onEmit, expectedGetSportResponse)

    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket()
    socketBuilder.clientSocket.on("IN_PLAY_SPORTS::16::LIVE_EVENT", { args -> onEmit.accept(args) })
    client = socketBuilder.initClient()
    JSONObject request = new JSONObject(("{\"categoryId\":16,\"isLiveNowType\":true,\"emptyTypes\":\"No\"," +
        "\"autoUpdates\":\"No\",\"topLevelType\":\"LIVE_EVENT\"}"))
    when:
    client.emit(GET_SPORT_REQUEST.messageId(), request)

    then:
    lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS)
    1 == getClientRooms(ioServer, client).size()
    "" == getClientRooms(ioServer, client).toArray()[0]
    //        AFTER THAT
    //        expectedGetSportResponse.setEventsByTypeName(expectedGetSportResponse.getEventsByTypeName()
    //                .stream().map({typeSegment->typeSegment.cloneWithEmptyTypes()}).collect(Collectors.toList()));
    //        lock = ioServerResponseVerification(onEmit, expectedGetSportResponse);
    //        socketBuilder.clientSocket.on("IN_PLAY_SPORTS::16::LIVE_EVENT", {args -> onEmit.accept(args)});
    //        request = new JSONObject(("{\"categoryId\":16,\"isLiveNowType\":true,\"emptyTypes\":\"Yes\"," +
    //                "\"autoUpdates\":\"Yes\",\"topLevelType\":\"LIVE_EVENT\"}"));
    //
    //        client.emit(GET_SPORT_REQUEST.messageId(), request)
    //
    //
    //        then:
    //        lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS)
    //        33 == getClientRooms(ioServer, client).size()
    //        "" == getClientRooms(ioServer, client).toArray()[0]
  }


  def getTypeTest() throws Exception {
    List<ModuleDataItem> expectedGetTypeResponse = listFromFile("response/get_type.json", ModuleDataItem.class)
    InPlayCache inPlayCache = fromFile("storage/InPlayCache.json", InPlayCache.class)
    cachedData.getSportSegments().putAll(inPlayCache.getSportSegmentCaches()
        .stream()
        .collect(Collectors.toMap({ sportSegmentCache -> sportSegmentCache.getStructuredKey() }, { sportSegmentCache -> sportSegmentCache })))
    CountDownLatch lock = ioServerResponseVerification(onEmit, expectedGetTypeResponse)

    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket()
    socketBuilder.clientSocket.on("IN_PLAY_SPORT_TYPE::16::LIVE_EVENT::442", { args -> onEmit.accept(args) })
    client = socketBuilder.initClient()
    when:
    JSONObject request = new JSONObject(("{\"categoryId\":16,\"isLiveNowType\":true,\"emptyTypes\":\"Yes\"," +
        "\"autoUpdates\":\"No\",\"topLevelType\":\"LIVE_EVENT\", \"typeId\":442}"))
    client.emit(GET_TYPE_REQUEST.messageId(), request)

    then:
    lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS) == true
    1 == getClientRooms(ioServer, client).size()
    "" == getClientRooms(ioServer, client).toArray()[0]
    //        AFTER THAT
    //        socketBuilder.clientSocket.on("IN_PLAY_SPORT_TYPE::7777::LIVE_EVENT::442", {args -> onEmit.accept(args)})
    //        request = new JSONObject(("{\"categoryId\":7777,\"isLiveNowType\":true,\"emptyTypes\":\"No\"," +
    //                "\"autoUpdates\":\"No\",\"topLevelType\":\"LIVE_EVENT\", \"typeId\":442}"))
    //        client.emit(GET_TYPE_REQUEST.messageId(), request)
    //
    //        then:
    //        lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS)
  }

  def cleanup() {
    if (client != null) {
      client.disconnect()
    }
    socketIOConnectorService.evict()
    ioServer.stop()
  }
}
