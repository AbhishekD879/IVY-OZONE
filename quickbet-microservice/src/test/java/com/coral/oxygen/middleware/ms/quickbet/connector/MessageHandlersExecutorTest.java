package com.coral.oxygen.middleware.ms.quickbet.connector;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.ERROR_CODE;
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.ErrorMessage;
import com.corundumstudio.socketio.SocketIOClient;
import java.util.UUID;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.function.Consumer;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;

class MessageHandlersExecutorTest {

  private static final int TIMEOUT = 1000;
  private final UUID sessionId = UUID.randomUUID();

  private SessionManager sessionManager = mock(SessionManager.class);
  private ExecutorService eventHandlingExecutor = Executors.newSingleThreadExecutor();

  private MessageHandlersExecutor messageHandlersExecutor =
      new MessageHandlersExecutor(sessionManager, eventHandlingExecutor);

  @Test
  @DisplayName("should call consumer if session exists")
  void testExecuteIfSessionExist() {
    // given
    SocketIOClient client = mock(SocketIOClient.class);
    when(client.getSessionId()).thenReturn(sessionId);

    Consumer<Session> consumer = mock(Consumer.class);

    Session session = mock(Session.class);
    when(sessionManager.getAttachedSession(eq(sessionId))).thenReturn(session);

    // when
    messageHandlersExecutor.executeIfSessionExist(client, consumer);

    // then

    verify(consumer, timeout(TIMEOUT)).accept(session);
  }

  @Test
  @DisplayName("should send error when no session found")
  void noSessionFound() {
    // given
    SocketIOClient client = mock(SocketIOClient.class);
    when(client.getSessionId()).thenReturn(null);

    Consumer<Session> consumer = mock(Consumer.class);

    Session session = mock(Session.class);
    when(sessionManager.getAttachedSession(eq(sessionId))).thenReturn(session);

    // when
    messageHandlersExecutor.executeIfSessionExist(client, consumer);

    // then

    ArgumentCaptor<ErrorMessage> captor = ArgumentCaptor.forClass(ErrorMessage.class);
    verify(client).sendEvent(eq("ERROR"), captor.capture());
    ErrorMessage errorMessage = captor.getValue();
    assertThat(errorMessage.getCode()).isEqualTo("1");
    assertThat(errorMessage.getMessage()).isEqualTo("Unauthorized connection");
  }

  @Test
  @DisplayName("should send error if consumer throws exception")
  void handleError() {
    // given
    SocketIOClient client = mock(SocketIOClient.class);
    when(client.getSessionId()).thenReturn(sessionId);

    Session session = mock(Session.class);
    when(sessionManager.getAttachedSession(eq(sessionId))).thenReturn(session);

    Consumer<Session> consumer = mock(Consumer.class);
    RuntimeException exception = new RuntimeException();
    doThrow(exception).when(consumer).accept(any());

    // when
    messageHandlersExecutor.executeIfSessionExist(client, consumer);

    // then

    verify(session, timeout(TIMEOUT)).sendData(eq(ERROR_CODE.code()), eq(exception.toString()));
  }
}
