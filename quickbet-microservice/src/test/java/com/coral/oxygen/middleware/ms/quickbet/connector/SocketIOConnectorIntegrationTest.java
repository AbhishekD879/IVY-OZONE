package com.coral.oxygen.middleware.ms.quickbet.connector;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.*;
import static org.mockito.Mockito.atLeastOnce;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.quickbet.BaseSession;
import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.configuration.SocketIOConfiguration;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.RegularPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.SessionDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.impl.QuickBetServiceV1;
import com.coral.oxygen.middleware.ms.quickbet.impl.QuickBetServiceV2;
import com.coral.oxygen.middleware.ms.quickbet.impl.SessionStorage;
import com.coral.oxygen.middleware.ms.quickbet.utils.WebSocketTestClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.protocol.JacksonJsonSupport;
import com.corundumstudio.socketio.protocol.JsonSupport;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.module.SimpleModule;
import com.fasterxml.jackson.databind.node.TextNode;
import com.google.gson.Gson;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.Executors;
import org.junit.jupiter.api.*;
import org.mockito.ArgumentCaptor;
import org.mockito.Mockito;
import org.mockito.stubbing.Answer;

class SocketIOConnectorIntegrationTest {

  private static final int PORT = 3434;
  // value taken from socketIoServer configuration
  private static final long PING_TIMEOUT = 60000;
  private static final String SESSION_ID = "gggd-5555dgg-4564";

  private static QuickBetServiceV1 quickBetServiceV1;
  private static QuickBetServiceV2 quickBetServiceV2;
  private static SessionManager sessionManager;
  private static MessageHandlersExecutor messageHandlersExecutor;
  private static Session session;

  private static SocketIOConnector socketIOConnector;

  private static WebSocketTestClient client;
  private static SocketIOServer socketIoServer;

  @BeforeAll
  static void setUp() {
    quickBetServiceV1 = Mockito.mock(QuickBetServiceV1.class);
    quickBetServiceV2 = Mockito.mock(QuickBetServiceV2.class);
    sessionManager = Mockito.mock(SessionManager.class);
    SessionStorage<SessionDto> sessionStorage = Mockito.mock(SessionStorage.class);
    session = new BaseSession(SESSION_ID, sessionStorage);

    SocketIOConfiguration configuration = new SocketIOConfiguration();
    socketIoServer =
        configuration.socketIOServer(PORT, addJsonSupport(configuration.gson()), 1, false, 0);

    when(sessionManager.getAttachedSession(any(UUID.class))).thenReturn(session);
    when(sessionManager.createAndAttachNewSession(any(UUID.class))).thenReturn(session);

    messageHandlersExecutor =
        new MessageHandlersExecutor(sessionManager, Executors.newFixedThreadPool(200));

    socketIOConnector =
        new SocketIOConnector(
            quickBetServiceV1,
            quickBetServiceV2,
            socketIoServer,
            sessionManager,
            messageHandlersExecutor);
    socketIOConnector.start();

    client = new WebSocketTestClient();
    client.start(PORT);
  }

  @AfterAll
  static void tearDown() {
    client.stop();
    socketIoServer.stop();
  }

  // I had to add custom deserializer module here, due to the bug with jackson mapper
  private static JsonSupport addJsonSupport(Gson gson) {

    SimpleModule outcomeActionModule = new SimpleModule();
    List<Class> deserializerClasses =
        Arrays.asList(RegularSelectionRequest.class, RegularPlaceBetRequest.class, Void.class);
    deserializerClasses.stream()
        .forEach(
            value -> {
              addDeserializer(gson, outcomeActionModule, value);
            });

    return new JacksonJsonSupport(outcomeActionModule) {
      @Override
      protected void init(ObjectMapper objectMapper) {
        super.init(objectMapper);
      }
    };
  }

  private static <T> void addDeserializer(Gson gson, SimpleModule module, Class<T> clazz) {
    module.addDeserializer(
        clazz,
        new JsonDeserializer<T>() {
          @Override
          public T deserialize(JsonParser p, DeserializationContext ctxt)
              throws IOException, JsonProcessingException {
            TextNode textNode = p.getCodec().readTree(p);
            return gson.fromJson(textNode.textValue(), clazz);
          }
        });
  }

  @BeforeEach
  public void initMocks() {
    when(sessionManager.getAttachedSession(any(UUID.class))).thenReturn(session);
    when(sessionManager.createAndAttachNewSession(any(UUID.class))).thenReturn(session);
  }

  @Test
  void testAddSelectionSingle() throws JsonProcessingException {
    Mockito.doAnswer(addServerCallbackAnswer(Messages.OUTCOME_REQUEST_CODE))
        .when(quickBetServiceV1)
        .addRegularSelection(eq(session), any(RegularSelectionRequest.class));
    client.emitRegularSelectionAction(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);

    ArgumentCaptor<RegularSelectionRequest> captor =
        ArgumentCaptor.forClass(RegularSelectionRequest.class);
    Mockito.verify(quickBetServiceV1, atLeastOnce())
        .addRegularSelection(eq(session), captor.capture());
    RegularSelectionRequest argument = captor.getValue();

    assertThat(argument.getOutcomeIds()).hasSize(2);
    assertThat(argument.getSelectionType())
        .isEqualTo(RegularSelectionRequest.SIMPLE_SELECTION_TYPE);
  }

  @Test
  void testPlaceFixedSGL() throws JsonProcessingException {
    Mockito.doAnswer(addServerCallbackAnswer(Messages.PLACE_BET_REQUEST_CODE))
        .when(quickBetServiceV1)
        .placeRegularBet(eq(session), any(RegularPlaceBetRequest.class));
    client.emitRegularPlaceBet();

    ArgumentCaptor<RegularPlaceBetRequest> captor =
        ArgumentCaptor.forClass(RegularPlaceBetRequest.class);
    Mockito.verify(quickBetServiceV1).placeRegularBet(eq(session), captor.capture());
    RegularPlaceBetRequest argument = captor.getValue();

    assertThat(argument.getPrice()).isEqualTo("1/2");
    assertThat(argument.getStake()).isEqualTo("2");
  }

  @Test
  void testClearSelection() {
    Mockito.doAnswer(addServerCallbackAnswer(Messages.CLEAR_SELECTION_REQUEST_CODE))
        .when(quickBetServiceV1)
        .clearSelection(session);
    client.emitClearSelection();

    Mockito.verify(quickBetServiceV1).clearSelection(session);
  }

  // This is unrealistic tests.
  // this method is required only for notifying client that server has consumed message.
  private Answer addServerCallbackAnswer(Messages message) {
    return invocation -> {
      session.sendData(message.code(), new Object());
      return null;
    };
  }
}
