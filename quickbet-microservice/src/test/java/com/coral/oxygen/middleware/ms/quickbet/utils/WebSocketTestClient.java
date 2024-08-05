package com.coral.oxygen.middleware.ms.quickbet.utils;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.LOGIN;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.LOGIN_SUCCESS;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.RegularPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.LoginRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.NewSessionResponse;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.socket.client.IO;
import io.socket.client.Socket;
import io.socket.engineio.client.transports.WebSocket;
import io.vavr.jackson.datatype.VavrModule;
import java.io.IOException;
import java.lang.reflect.Type;
import java.net.URI;
import java.util.Arrays;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.json.JSONString;
import org.springframework.web.util.UriComponentsBuilder;

/**
 * This class is intended to use in conjunction with SocketIOConnectorIntegrationTest.java . It
 * setups simple webSocket client that emits various messages defined in Messages.java enum.
 */
@Slf4j
public class WebSocketTestClient {

  private static final String DEFAULT_URL = "http://localhost";
  private ExecutorService executorService;

  private volatile boolean connectionReceived = false;
  private volatile boolean connected = false;
  private Socket socket;
  private ObjectMapper mapper;

  private String sessionId;

  private ConcurrentHashMap<String, Object> receivedDataMap;

  public WebSocketTestClient() {
    mapper = new ObjectMapper();
    mapper.registerModule(new VavrModule());
    receivedDataMap = new ConcurrentHashMap<>();
  }

  public void start(int port) {
    start(port, null, null);
    NewSessionResponse newSessionResponse =
        wait(Messages.NEW_SESSION_CODE, NewSessionResponse.class);
    this.sessionId = newSessionResponse.getId();
  }

  public void start(int port, String sessionId) {
    start(port, sessionId, null);
  }

  public void start(int port, String sessionId, String bppToken) {
    executorService = Executors.newFixedThreadPool(1);
    initializeSocket(port, sessionId, bppToken);
    setupEventListeners();
    socket.connect();
    waitForConnectionEvent();
    this.sessionId = sessionId;
  }

  private void initializeSocket(int port, String sessionId, String bppToken) {
    IO.Options options = prepareSocketConfigurations();
    socket = IO.socket(buildUri(port, sessionId, bppToken), options);
  }

  private URI buildUri(int port, String sessionId, String bppToken) {
    UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl(DEFAULT_URL).port(port);

    if (StringUtils.isNotEmpty(sessionId)) {
      builder.queryParam("id", sessionId);
    }
    if (StringUtils.isNotEmpty(bppToken)) {
      builder.queryParam("token", bppToken);
    }
    return builder.build().toUri();
  }

  // set listeners for some events, we would like to verify
  private void setupEventListeners() {
    socket.on(
        Socket.EVENT_CONNECT,
        objects -> {
          connectionReceived = true;
          connected = true;
        });
    socket.on("ERROR", args -> putToReceivedMessages("ERROR", args[0].toString()));
    socket.on(Socket.EVENT_DISCONNECT, args -> connected = false);
    Stream.of(Messages.values()).forEach(this::addListener);
  }

  private IO.Options prepareSocketConfigurations() {
    IO.Options options = new IO.Options();

    options.path = "/quickbet";
    options.query = "{}";
    options.transports = new String[] {WebSocket.NAME};
    options.upgrade = false;
    options.reconnectionDelay = 1000 * 100;
    options.forceNew = false;
    options.timeout = 5000 * 100;
    options.reconnectionAttempts = 1;

    return options;
  }

  private void addListener(Messages message) {
    socket.on(message.code(), args -> putToReceivedMessages(message.code(), args[0].toString()));
  }

  private void waitForConnectionEvent() {
    Future future =
        Executors.newSingleThreadExecutor()
            .submit(
                () -> {
                  while (!connectionReceived) {
                    try {
                      Thread.sleep(50);
                    } catch (InterruptedException e) {
                      break;
                    }
                  }
                  connectionReceived = false;
                });
    try {
      future.get(60, TimeUnit.SECONDS);
    } catch (ExecutionException | TimeoutException e) {
      throw new RuntimeException("There is no EVENT_CONNECT event from the server", e);
    } catch (InterruptedException e) {
      throw new RuntimeException("Interruption during connect attempt ", e);
    }
  }

  // ensuring, that server got the message
  private void waitForEvent(Messages message) {
    while (!receivedDataMap.containsKey(message.code())) {
      if (receivedDataMap.containsKey(Messages.ERROR_CODE.code())) {
        throw new RuntimeException(
            "Error received " + receivedDataMap.get(Messages.ERROR_CODE.code()));
      }
      try {
        Thread.sleep(50);
      } catch (InterruptedException e) {
        break;
      }
    }
  }

  /**
   * Wait for message to be received by client. To get received message use {@link
   * WebSocketTestClient#getReceivedData(Messages)}
   *
   * @param message to wait for
   */
  public void wait(Messages message) {
    try {
      executorService.submit(() -> waitForEvent(message)).get();
    } catch (ExecutionException e) {
      log.error(
          "Error occurred while waiting for the message [{}]\n Data map state: {} ",
          message.code(),
          receivedDataMap.toString());
      throw new RuntimeException(e.getCause());
    } catch (InterruptedException e) {
      log.error("Interruption occurred while waiting for the message [{}] ", message.code(), e);
      throw new RuntimeException("Interruption occurred while waiting for the message", e);
    }
  }

  public <T> T wait(Messages message, Class<T> responseClass) {
    return wait(
        message,
        new TypeReference<T>() {
          @Override
          public Type getType() {
            return responseClass;
          }
        });
  }

  /**
   * Wait for message to be received by client. After receiving <strong>clear</strong> all received
   * data.
   *
   * @param message to wait for
   * @param responseClass specified type
   * @return Transformed to specified type
   */
  public <T> T wait(Messages message, TypeReference<T> responseClass) {
    wait(message);
    String data = getReceivedData(message.code()).toString();
    clearReceivedData();
    try {
      return mapper.readValue(data, responseClass);
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  public void stop() {
    socket.disconnect();
    executorService.shutdown();
    try {
      if (!executorService.awaitTermination(1, TimeUnit.SECONDS)) {
        executorService.shutdownNow();
      }
    } catch (InterruptedException e) {
      executorService.shutdownNow();
    }
    log.info("test client stopped.");
  }

  public void emitRegularSelectionAction(String selectionType) throws JsonProcessingException {
    RegularSelectionRequest request = new RegularSelectionRequest();
    request.setOutcomeIds(Arrays.asList(12345L, 6789L));
    request.setSelectionType(selectionType);
    RegularSelectionRequest.AdditionalParameters additionalParameters =
        new RegularSelectionRequest.AdditionalParameters();
    additionalParameters.setScorecastMarketId(12345L);
    request.setAdditional(additionalParameters);

    socket.emit(Messages.OUTCOME_REQUEST_CODE.code(), mapper.writeValueAsString(request));
    waitForEvent(Messages.OUTCOME_REQUEST_CODE);
  }

  public <T> T emitWithWaitForResponse(
      Messages messages, Object request, Messages waitForMessage, Class<T> responseClass) {
    return emitWithWaitForResponse(
        messages,
        request,
        waitForMessage,
        new TypeReference<T>() {
          @Override
          public Type getType() {
            return responseClass;
          }
        });
  }

  public void emitWithWaitForResponse(Messages messages, Object object, Messages waitForMessage) {
    try {
      emit(messages, object);
      wait(waitForMessage);
    } catch (JsonProcessingException e) {
      throw new RuntimeException(e);
    }
  }

  public <T> T emitWithWaitForResponse(
      Messages messages, Object object, Messages waitForMessage, TypeReference<T> typeReference) {
    try {
      emit(messages, object);
      return wait(waitForMessage, typeReference);
    } catch (JsonProcessingException e) {
      throw new RuntimeException(e);
    }
  }

  public <T> T emitWithWaitForResponse(
      Messages messages, String jsonAsString, Messages waitForMessage, Class<T> responseClass) {
    emit(messages, jsonAsString);
    return wait(waitForMessage, responseClass);
  }

  public void emit(Messages message, String jsonAsString) {
    socket.emit(message.code(), (JSONString) () -> jsonAsString);
  }

  public void emit(Messages message, Object request) throws JsonProcessingException {
    String valueAsJSONString = mapper.writeValueAsString(request);
    socket.emit(message.code(), (JSONString) () -> valueAsJSONString);
  }

  public void emitUnauth() {
    socket.emit(Messages.PLACE_BET_REQUEST_CODE.code(), new RegularPlaceBetRequest());
    waitForEvent(Messages.ERROR_CODE);
  }

  public void emitRegularPlaceBet() throws JsonProcessingException {
    RegularPlaceBetRequest request = new RegularPlaceBetRequest();
    request.setPrice("1/2");
    request.setStake("2");
    request.setToken("fsdffsfsdffgs");

    socket.emit(Messages.PLACE_BET_REQUEST_CODE.code(), mapper.writeValueAsString(request));
    waitForEvent(Messages.PLACE_BET_REQUEST_CODE);
  }

  public void emitClearSelection() {
    socket.emit(Messages.CLEAR_SELECTION_REQUEST_CODE.code(), "");
    waitForEvent(Messages.CLEAR_SELECTION_REQUEST_CODE);
  }

  public Object getReceivedData(String key) {
    return receivedDataMap.get(key);
  }

  public Object getReceivedData(Messages message) {
    return getReceivedData(message.code());
  }

  public <T> T getReceivedData(Messages message, Class<T> responseClass) {
    try {
      return mapper.readValue(getReceivedData(message).toString(), responseClass);
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  public void putToReceivedMessages(String code, String arg) {
    receivedDataMap.put(code, arg);
  }

  public void clearReceivedData() {
    receivedDataMap.clear();
  }

  public String getSessionId() {
    return this.sessionId;
  }

  public boolean isConnected() {
    return connected;
  }

  public void login(String bppToken) {
    emitWithWaitForResponse(LOGIN, new LoginRequest(bppToken), LOGIN_SUCCESS);
  }
}
