package com.coral.oxygen.middleware.ms.quickbet.connector;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.ERROR_CODE;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.corundumstudio.socketio.SocketIOClient;
import com.newrelic.api.agent.NewRelic;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;
import java.util.function.Consumer;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.slf4j.MDC;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

@Component
public class MessageHandlersExecutor {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  private final SessionManager sessionManager;
  private final Executor eventHandlingExecutor;

  public MessageHandlersExecutor(
      SessionManager sessionManager,
      @Qualifier("eventHandlingExecutorService") Executor eventHandlingExecutor) {
    this.sessionManager = sessionManager;
    this.eventHandlingExecutor = eventHandlingExecutor;
  }

  public void executeIfSessionExist(SocketIOClient client, Consumer<Session> consumer) {
    Session session = sessionManager.getAttachedSession(client.getSessionId());
    if (Objects.isNull(session)) {
      sendUnauthorizedError(client);
    } else {
      NewRelic.incrementCounter("Custom/executeIfSessionExist");
      MDC.put("session", session.sessionId());

      Map<String, String> copyOfContextMap = MDC.getCopyOfContextMap();
      CompletableFuture.runAsync(
              () -> {
                MDC.setContextMap(copyOfContextMap);
                consumer.accept(session);
              },
              eventHandlingExecutor)
          .whenCompleteAsync(
              (success, error) -> {
                MDC.setContextMap(copyOfContextMap);
                if (error != null) {
                  ASYNC_LOGGER.error(
                      "Error from completable future in session: {} ",
                      session.sessionId(),
                      error.getCause());
                  session.sendData(ERROR_CODE.code(), error.getMessage());
                } else {
                  ASYNC_LOGGER.info("Completed async task in session: {}", session.sessionId());
                }
                MDC.clear();
              });
    }
  }

  private void sendUnauthorizedError(SocketIOClient client) {
    ASYNC_LOGGER.info("Unauthorized Error {}", client.getSessionId());
    client.sendEvent(ERROR_CODE.code(), ErrorMessageFactory.unauthorizedConnection());
  }
}
