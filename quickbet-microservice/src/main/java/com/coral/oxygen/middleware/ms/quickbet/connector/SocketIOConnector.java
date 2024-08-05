package com.coral.oxygen.middleware.ms.quickbet.connector;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.*;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.SessionListener;
import com.coral.oxygen.middleware.ms.quickbet.SessionNotFoundException;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.LuckyDipBetPlacementRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.RegularPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachPlaceBetRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachSelectionRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.FreeBetForChannelRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.UIPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.AddComplexSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.AddSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.LoginRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.RemoveComplexSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.NewSessionResponse;
import com.coral.oxygen.middleware.ms.quickbet.impl.QuickBetServiceV1;
import com.coral.oxygen.middleware.ms.quickbet.impl.QuickBetServiceV2;
import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.google.gson.Gson;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.util.Collection;
import java.util.UUID;
import org.apache.logging.log4j.Level;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Component;

@Component
public final class SocketIOConnector {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  private static final String SESSION_ID_PARAMETER_NAME = "id";
  private static final String BPP_TOKEN_PARAMETER_NAME = "token";
  private boolean started;

  private final QuickBetServiceV1 quickBetServiceV1;
  private final QuickBetServiceV2 quickBetServiceV2;

  private final SocketIOServer socketIoServer;
  private final SessionManager sessionManager;
  private final MessageHandlersExecutor messageHandlersExecutor;

  public SocketIOConnector(
      QuickBetServiceV1 quickBetServiceV1,
      QuickBetServiceV2 quickBetServiceV2,
      SocketIOServer socketIoServer,
      SessionManager sessionManager,
      MessageHandlersExecutor messageHandlersExecutor) {
    this.quickBetServiceV1 = quickBetServiceV1;
    this.quickBetServiceV2 = quickBetServiceV2;
    this.socketIoServer = socketIoServer;
    this.sessionManager = sessionManager;
    this.messageHandlersExecutor = messageHandlersExecutor;
  }

  public void start() {
    if (!started) {
      configureConnection();
      configureDisconnection();
      socketIoServer.addEventListener(LOGIN.code(), LoginRequest.class, this::onLogin);
      socketIoServer.addEventListener(LOGOUT.code(), Void.class, this::onLogout);
      socketIoServer.addEventListener(
          OUTCOME_REQUEST_CODE.code(),
          RegularSelectionRequest.class,
          this::onAddRegularSelectionAction);
      socketIoServer.addEventListener(
          PLACE_BET_REQUEST_CODE.code(),
          RegularPlaceBetRequest.class,
          this::onReqularPlaceBetAction);
      socketIoServer.addEventListener(
          CLEAR_SELECTION_REQUEST_CODE.code(), Void.class, this::onClearSelectionAction);
      socketIoServer.addEventListener(
          Messages.ADD_BANACH_SELECTION.code(),
          BanachSelectionRequestData.class,
          this::onAddBanachSelection);
      socketIoServer.addEventListener(
          Messages.BANACH_PLACE_BET.code(), BanachPlaceBetRequestData.class, this::placeBanachBet);
      socketIoServer.addEventListener(
          Messages.FREE_BET_FOR_CHANNEL.code(),
          FreeBetForChannelRequestData.class,
          this::onAddFreeBetsForChannel);
      socketIoServer.addEventListener(
          REMOVE_ONE_SELECTION.code(), String.class, this::removeOneSelection);
      socketIoServer.addEventListener(
          ADD_SELECTION.code(), AddSelectionRequest.class, this::addSelection);
      socketIoServer.addEventListener(
          ADD_COMPLEX_SELECTION.code(),
          AddComplexSelectionRequest.class,
          this::addComplexSelection);
      socketIoServer.addEventListener(
          REMOVE_COMPLEX_SELECTION.code(),
          RemoveComplexSelectionRequest.class,
          this::removeComplexSelection);
      socketIoServer.addEventListener(PLACE_BET.code(), UIPlaceBetRequest.class, this::placeBet);
      socketIoServer.addEventListener(
          LUCKY_DIP_PLACE_BET_REQUEST_CODE.code(),
          LuckyDipBetPlacementRequest.class,
          this::onLuckyDipPlaceBetAction);
      socketIoServer.start();
      started = true;
    }
  }

  public void stop() {
    if (started) {
      sessionManager.getAllAttachedSessions().keySet().forEach(sessionManager::detachSession);
      socketIoServer.stop();
      started = false;
    }
  }

  private void doConnect(SocketIOClient client) {
    String qbsid =
        client.getHandshakeData().getSingleUrlParam(SocketIOConnector.SESSION_ID_PARAMETER_NAME);
    String bppToken =
        client.getHandshakeData().getSingleUrlParam(SocketIOConnector.BPP_TOKEN_PARAMETER_NAME);
    ASYNC_LOGGER.debug("Client connected SISID: {}, QBSID {}", client.getSessionId(), qbsid);
    try {
      Session session;
      if (qbsid == null) {
        session = sessionManager.createAndAttachNewSession(client.getSessionId());
        ASYNC_LOGGER.log(Level.INFO, () -> "Sending new session id: " + session.sessionId());
        client.sendEvent(NEW_SESSION_CODE.code(), new NewSessionResponse(session.sessionId()));
        setupListener(client, session);
      } else {
        session = sessionManager.loadPersistedSession(qbsid);
        sessionManager.attachSession(client.getSessionId(), session);
        setupListener(client, session);
        quickBetServiceV1.restoreState(session, bppToken);
      }
      NewRelic.incrementCounter("Custom/doConnect");
    } catch (SessionNotFoundException ex) {
      ASYNC_LOGGER.warn("Session not found", ex);
      client.sendEvent(ERROR_CODE.code(), ErrorMessageFactory.sessionNotFound());
      client.disconnect();
      NewRelic.noticeError(ex);
    }
  }

  private void setupListener(SocketIOClient client, Session session) {
    session.setListener(
        new SessionListener() {
          @Override
          public void subscribeToRooms(Collection<String> names) {
            names.stream().forEach(client::joinRoom);
          }

          @Override
          public void unsubscribeFromRooms(Collection<String> names) {
            names.forEach(client::leaveRoom);
          }

          @Override
          public void sendData(String message, Object data) {
            ASYNC_LOGGER.info("Sending data to client {} : {}", message, new Gson().toJson(data));
            client.sendEvent(message, data);
          }
        });
  }

  private void configureConnection() {
    socketIoServer.addConnectListener(this::doConnect);
  }

  private void configureDisconnection() {
    socketIoServer.addDisconnectListener(this::onDisconnect);
  }

  private void onDisconnect(SocketIOClient client) {
    UUID clientSessionId = client.getSessionId();
    ASYNC_LOGGER.debug("Client disconnected {}", clientSessionId);
    sessionManager.detachSession(clientSessionId);
    NewRelic.incrementCounter("Custom/onDisconnect");
  }

  @Trace(dispatcher = true)
  private void onLogin(SocketIOClient client, LoginRequest request, AckRequest ackRequest) {
    messageHandlersExecutor.executeIfSessionExist(
        client, session -> quickBetServiceV2.login(session, request.getToken()));
  }

  @Trace(dispatcher = true)
  private void onLogout(SocketIOClient client, Object object, AckRequest ackRequest) {
    messageHandlersExecutor.executeIfSessionExist(client, quickBetServiceV2::logout);
  }

  @Trace(dispatcher = true)
  private void onAddRegularSelectionAction(
      SocketIOClient client, RegularSelectionRequest request, AckRequest ackRequest) {
    messageHandlersExecutor.executeIfSessionExist(
        client, session -> quickBetServiceV1.addRegularSelection(session, request));
  }

  @Trace(dispatcher = true)
  private void onReqularPlaceBetAction(
      SocketIOClient client, RegularPlaceBetRequest request, AckRequest ackRequest) {
    messageHandlersExecutor.executeIfSessionExist(
        client, session -> quickBetServiceV1.placeRegularBet(session, request));
  }

  @Trace(dispatcher = true)
  private void onClearSelectionAction(SocketIOClient client, Void t, AckRequest ackRequest) {
    messageHandlersExecutor.executeIfSessionExist(client, quickBetServiceV1::clearSelection);
  }

  @Trace(dispatcher = true)
  private void onAddBanachSelection(
      SocketIOClient client, BanachSelectionRequestData requestData, AckRequest ackRequest) {
    messageHandlersExecutor.executeIfSessionExist(
        client, session -> quickBetServiceV1.addBanachSelection(session, requestData));
  }

  @Trace(dispatcher = true)
  private void placeBanachBet(
      SocketIOClient client, BanachPlaceBetRequestData requestData, AckRequest ackRequest) {
    messageHandlersExecutor.executeIfSessionExist(
        client, session -> quickBetServiceV1.placeBanachBet(session, requestData));
  }

  @Trace(dispatcher = true, nameTransaction = true)
  private void onAddFreeBetsForChannel(
      SocketIOClient client, FreeBetForChannelRequestData requestData, AckRequest ackRequest) {
    messageHandlersExecutor.executeIfSessionExist(
        client, session -> quickBetServiceV1.addFreeBetTokensForChannel(session, requestData));
  }

  @Trace(dispatcher = true)
  private void removeOneSelection(SocketIOClient client, String outcomeId, AckRequest ackRequest) {
    messageHandlersExecutor.executeIfSessionExist(
        client, session -> quickBetServiceV2.removeOneSelection(session, outcomeId));
  }

  @Trace(dispatcher = true)
  private void addSelection(
      SocketIOClient client, AddSelectionRequest request, AckRequest ackRequest) {
    messageHandlersExecutor.executeIfSessionExist(
        client, session -> quickBetServiceV2.addSelection(session, request));
  }

  @Trace(dispatcher = true)
  private void addComplexSelection(
      SocketIOClient client, AddComplexSelectionRequest request, AckRequest ackRequest) {
    messageHandlersExecutor.executeIfSessionExist(
        client, session -> quickBetServiceV2.addComplexSelection(session, request));
  }

  @Trace(dispatcher = true)
  private void removeComplexSelection(
      SocketIOClient client, RemoveComplexSelectionRequest request, AckRequest ackRequest) {
    messageHandlersExecutor.executeIfSessionExist(
        client, session -> quickBetServiceV2.removeComplexSelection(session, request));
  }

  @Trace(dispatcher = true)
  private void placeBet(
      SocketIOClient client, UIPlaceBetRequest placeBetRequest, AckRequest ackRequest) {
    messageHandlersExecutor.executeIfSessionExist(
        client, session -> quickBetServiceV2.placeBet(session, placeBetRequest));
  }

  @Trace(dispatcher = true)
  private void onLuckyDipPlaceBetAction(
      SocketIOClient client, LuckyDipBetPlacementRequest request, AckRequest ackRequest) {
    messageHandlersExecutor.executeIfSessionExist(
        client, session -> quickBetServiceV1.placeLuckyDipBet(session, request));
  }
}
