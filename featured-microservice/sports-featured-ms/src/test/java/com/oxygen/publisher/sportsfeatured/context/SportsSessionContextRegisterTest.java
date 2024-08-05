package com.oxygen.publisher.sportsfeatured.context;

import static com.oxygen.publisher.sportsfeatured.context.SportsSocketMessages.PAGE_SWITCH;
import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.*;

import com.corundumstudio.socketio.HandshakeData;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.oxygen.publisher.configuration.JsonSupportConfig;
import com.oxygen.publisher.configuration.SocketIOConnectorConfiguration;
import com.oxygen.publisher.configuration.SocketIOServerConfiguration;
import com.oxygen.publisher.model.ApplicationVersion;
import com.oxygen.publisher.server.SocketIOConnector;
import com.oxygen.publisher.server.config.SocketBuilder;
import com.oxygen.publisher.sportsfeatured.configuration.FeaturedServiceConfiguration;
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import io.socket.client.Socket;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.function.Consumer;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Answers;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(MockitoJUnitRunner.class)
public class SportsSessionContextRegisterTest {
  @Mock(answer = Answers.RETURNS_DEEP_STUBS)
  private SportsMiddlewareContext sportsMiddlewareContext;

  private SportsCachedData sportsCachedData;
  @Mock SportsSessionContext sportsSessionContext;

  private Socket client;
  private SocketIOClient socketIOClient;
  private SocketIOServer socketIOServer;
  private HandshakeData handshakeData;

  private SocketIOConnector socketIOConnectorService;

  private Consumer<Object[]> onEmit;

  @Before
  public void init() {
    /*FeaturedModel featuredModel = createStructureWithSegmentWiseModules("16");
    sportsCachedData = new SportsCachedData(25, 20);
    sportsCachedData.getStructureMap().put(PageRawIndex.forSport(16), featuredModel);
    sportsCachedData.insertSportPageData(SocketIoTestHelper.getSportPageMapCache());*/
    // FeaturedModel featuredModel = createStructureWithSegmentWiseModules("16");

    sportsCachedData = spy(new SportsCachedData(44, 22));
    //
    // doNothing().when(sportsCachedData).insertSportPageData(SocketIoTestHelper.getSportPageMapCache());
    doReturn(sportsCachedData).when(sportsMiddlewareContext).getFeaturedCachedData();

    //
    // doReturn(featuredModel).when(sportsCachedData).getStructure(PageRawIndex.fromPageId("16"));

    // Mockito.when(sportsMiddlewareContext.getFeaturedCachedData()).thenReturn(sportsCachedData);
    socketIOServer = mock(SocketIOServer.class);
    client = mock(Socket.class);
    handshakeData = mock(HandshakeData.class);
    socketIOClient = mock(SocketIOClient.class);
    SocketIOConnectorConfiguration connectorConf = spy(new SocketIOConnectorConfiguration());
    FeaturedServiceConfiguration serviceConfiguration = spy(new FeaturedServiceConfiguration());
    SocketIOServerConfiguration serverConfig = new SocketIOServerConfiguration();

    JsonSupportConfig liveServeUtilsConfig = new JsonSupportConfig();

    ObjectMapper mapper = liveServeUtilsConfig.objectMapper();
    mapper.configure(SerializationFeature.FAIL_ON_EMPTY_BEANS, false);
    socketIOConnectorService =
        connectorConf.socketIOConnector(
            serverConfig.socketIOServer(
                8083, false, 1, 1, "/websocket", liveServeUtilsConfig.jsonSupport(mapper), 512),
            serviceConfiguration.featuredSessionContext(
                new ApplicationVersion("100.0"), sportsMiddlewareContext));
    socketIOConnectorService.start();
    socketIOServer =
        (SocketIOServer) ReflectionTestUtils.getField(socketIOConnectorService, "server");
    socketIOServer.start();
    onEmit = mock(Consumer.class);
  }

  @Test
  public void onSubscribeSport() throws Exception {

    CountDownLatch lock = new CountDownLatch(1);
    SocketBuilder socketBuilder =
        new SocketBuilder()
            .connectionUrl("http://localhost:8083", "transport=websocket&EIO=3", "/websocket");
    socketBuilder.clientSocket.on("version", args -> onEmit.accept(args));
    client = socketBuilder.initClient();
    // assertThat(lock.await(20, TimeUnit.SECONDS)).isTrue();
    assertEquals(1, getClientRooms(socketIOServer, client).size());
    assertEquals("", getClientRooms(socketIOServer, client).toArray()[0]);

    final String serverResponse = "Data for subscribed clients";
    // lock = ioServerResponseVerification(onEmit, serverResponse);
    // socketBuilder.clientSocket.on("EventId", args -> onEmit.accept(args));

    /*assertEquals(1, getClientRooms(socketIOServer, client).size());
    assertEquals("", getClientRooms(socketIOServer, client).toArray()[0]);*/
    // doNothing().when(sportsSessionContext).switchSportPages(socketIOClient, "16");
    client.emit(PAGE_SWITCH.messageId(), "16");
    lock.await(5, TimeUnit.SECONDS);
    assertEquals(1, getClientRooms(socketIOServer, client).size());
  }

  /*FeaturedModel createStructureWithSegmentWiseModules(String pageId) {
    FeaturedModel model = new FeaturedModel(pageId);
    Map<String, SegmentView> segmentWiseModules = new HashMap<>();
    SegmentView segmentView = new SegmentView();
    HighlightCarouselModule highlightCarouselModule =
        createHighlightCarouselModule("Highlight Carousel");
    model.addModule(highlightCarouselModule);
    SegmentOrderdModule segmentOrderdModuleForHc =
        new SegmentOrderdModule(1, highlightCarouselModule);
    segmentView
        .getHighlightCarouselModules()
        .put(highlightCarouselModule.getId(), segmentOrderdModuleForHc);

    segmentWiseModules.put("segment", segmentView);
    model.setSegmentWiseModules(segmentWiseModules);
    return model;
  }
  HighlightCarouselModule createHighlightCarouselModule(String id) {
    HighlightCarouselModule module = new HighlightCarouselModule();
    module.setType("HighlightCarouselModule");
    module.setId(id);
    SurfaceBetModuleData data = new SurfaceBetModuleData();
    data.setId("123");
    ArrayList list = new ArrayList();
    list.add(data);
    module.setData(list);
    return module;
  }*/

  public static Set<String> getClientRooms(SocketIOServer ioServer, Socket client) {
    return ioServer.getClient(UUID.fromString(client.id())).getAllRooms();
  }
}
