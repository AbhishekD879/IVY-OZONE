package com.oxygen.publisher.service.impl

import com.corundumstudio.socketio.SocketIOServer
import com.fasterxml.jackson.databind.ObjectMapper
import com.oxygen.publisher.configuration.JsonSupportConfig
import com.oxygen.publisher.configuration.SocketIOConnectorConfiguration
import com.oxygen.publisher.configuration.SocketIOServerConfiguration
import com.oxygen.publisher.inplay.configuration.InplayServiceConfiguration
import com.oxygen.publisher.inplay.context.InplayMiddlewareContext
import com.oxygen.publisher.inplay.context.InplaySessionContext
import com.oxygen.publisher.model.InPlayData
import com.oxygen.publisher.model.InplayCachedData
import com.oxygen.publisher.server.SocketIOConnector
import com.oxygen.publisher.server.config.SocketBuilder
import io.socket.client.Socket
import org.skyscreamer.jsonassert.JSONAssert
import org.springframework.test.util.ReflectionTestUtils
import spock.lang.Ignore
import spock.lang.Specification

import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import java.util.function.Consumer


import static com.oxygen.publisher.server.config.UnitTestUtil.fromFile
import static com.oxygen.publisher.server.config.UnitTestUtil.getClientRooms
import static com.oxygen.publisher.inplay.context.InplaySocketMessages.GET_INPLAY_STRUCTURE_REQUEST;
import static com.oxygen.publisher.inplay.context.InplaySocketMessages.GET_INPLAY_STRUCTURE_RESPONSE;

@Ignore
class InPlaySessionContextExtraSpec extends Specification {
  SocketIOConnector socketIOConnectorService
  InplaySessionContext sessionContext

  InplayMiddlewareContext middlewareContext

  InPlayData inPlayData
  InplayCachedData cachedData
  Socket client

  Consumer<Object[]> onEmit
  SocketIOServer ioServer

  String appVersion = "85.0.0"
  static final String IN_PLAY_SERVER_CONTEXT = "/websocket"
  static final int SOCKET_TIMEOUT = 10

  JsonSupportConfig liveServeUtilsConfig = new JsonSupportConfig()
  private ObjectMapper objectMapper = new JsonSupportConfig().objectMapper();


  def setup(){
    // prepare some inplay middleware context to pass to socket.io connector
    cachedData = Spy(new InplayCachedData())
    inPlayData = fromFile("response/get_inplay_structure.json", InPlayData.class)
    cachedData.getStructure() >> fromFile("response/get_inplay_structure.json", InPlayData.class)
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

  private CountDownLatch ioServerResponseVerification(Consumer<Object[]> onEmit, Object expectedResponse) {
    CountDownLatch lock = new CountDownLatch(1);

    onEmit.accept(_) >> { arguments ->
      // server response
      Object[] msg = arguments[0]
      assert msg.length > 0
      JSONAssert.assertEquals(objectMapper.writeValueAsString(expectedResponse), String.valueOf(msg[0]), true)
      lock.countDown()

      return msg
    }

    return lock;
  }

  def getInplayStructureTest() throws Exception {
    CountDownLatch lock = ioServerResponseVerification(onEmit, inPlayData)
    when:
    SocketBuilder socketBuilder = SocketBuilder.getInplaySocket()
    socketBuilder.clientSocket.on(GET_INPLAY_STRUCTURE_RESPONSE.messageId(), { args -> onEmit.accept(args) })
    client = socketBuilder.initClient()
    client.emit(GET_INPLAY_STRUCTURE_REQUEST.messageId())

    then:
    lock.await(SOCKET_TIMEOUT, TimeUnit.SECONDS)
    1 == getClientRooms(ioServer, client).size()
    "" == getClientRooms(ioServer, client).toArray()[0]
  }

  def cleanup() {
    if (client != null) {
      client.disconnect()
    }
    socketIOConnectorService.evict()
    ioServer.stop()
  }
}
