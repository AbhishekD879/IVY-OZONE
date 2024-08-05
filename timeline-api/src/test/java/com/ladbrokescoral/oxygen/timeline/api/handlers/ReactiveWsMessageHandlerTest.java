package com.ladbrokescoral.oxygen.timeline.api.handlers;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.timeline.api.channel.ChannelHandlersContext;
import com.ladbrokescoral.oxygen.timeline.api.controller.Room;
import com.ladbrokescoral.oxygen.timeline.api.reactive.model.MessageContent;
import java.util.*;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.messaging.Message;
import org.springframework.web.reactive.socket.WebSocketMessage;
import org.springframework.web.reactive.socket.WebSocketSession;
import reactor.core.Disposable;
import reactor.core.Disposables;
import reactor.core.publisher.FluxSink;
import reactor.core.publisher.Sinks;

@RunWith(MockitoJUnitRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class ReactiveWsMessageHandlerTest {
  @Mock private WebSocketSession session;
  @Mock private FluxSink<WebSocketMessage> sink;
  @Mock WebSocketMessage webSocketMessage;
  private Map<String, Disposable> disposablesOfAllSubscribedChannels = new HashMap<>();
  private String channelId = Room.ACTION_ROOM.name();

  @InjectMocks
  private ReactiveWsMessageHandler handler =
      new ReactiveWsMessageHandler(session, sink, disposablesOfAllSubscribedChannels);

  @Test
  public void testHandleMessage() {
    when(session.textMessage(anyString())).thenReturn(webSocketMessage);
    handler.handleMessage(new MessageContent("content"));
    verify(sink, times(1)).next(webSocketMessage);
  }

  @Test
  public void testAddSubscription() {
    Arrays.stream(Room.values())
        .forEach(room -> ChannelHandlersContext.createIfAbsentAndReturnChannel(room.name()));

    handler.addSubscriptionToAllRooms();
    assertNotNull(disposablesOfAllSubscribedChannels.get(channelId));
  }

  @Test
  public void testCleanUpCurrentPageContext() {
    Map<String, Disposable> disposablesOfAllSubscribedChannels = new HashMap<>();
    disposablesOfAllSubscribedChannels.put(channelId, Disposables.single());
    handler = new ReactiveWsMessageHandler(session, sink, disposablesOfAllSubscribedChannels);
    ChannelHandlersContext.getMessageHandlersPerPage().put(channelId, createMessageHandler());
    handler.cleanUpCurrentPageContext();
    assertNull(disposablesOfAllSubscribedChannels.get(channelId));
  }

  @Test
  public void testCleanUpCurrentPageContextDisposableNull() {
    Map<String, Disposable> disposablesOfAllSubscribedChannels = new HashMap<>();
    disposablesOfAllSubscribedChannels.put(channelId, null);
    handler = new ReactiveWsMessageHandler(session, sink, disposablesOfAllSubscribedChannels);
    ChannelHandlersContext.getMessageHandlersPerPage().put(channelId, createMessageHandler());
    handler.cleanUpCurrentPageContext();
    assertNull(disposablesOfAllSubscribedChannels.get(channelId));
  }

  @Test
  public void testCloseConnection() {
    handler.closeConnection();
    verify(sink).complete();
  }

  @Test
  public void testErrorHandling() {
    Arrays.stream(Room.values())
        .forEach(room -> ChannelHandlersContext.createIfAbsentAndReturnChannel(room.name()));
    Sinks.Many<Message<?>> sink =
        ChannelHandlersContext.getChannels().entrySet().stream()
            .findFirst()
            .get()
            .getValue()
            .get(0);
    handler.addSubscriptionToAllRooms();
    sink.tryEmitError(new RuntimeException());

    assertNotNull(disposablesOfAllSubscribedChannels.get(channelId));
  }

  @Test
  public void testEquals() {

    handler.equals(handler);
    handler.equals(null);
    boolean result = handler.equals(new Object());

    assertFalse(result);
  }

  private Set<ReactiveWsMessageHandler> createMessageHandler() {

    ReactiveWsMessageHandler handler = ReactiveWsMessageHandler.builder().session(session).build();
    Set<ReactiveWsMessageHandler> set = new HashSet<>();
    set.add(handler);
    return set;
  }
}
