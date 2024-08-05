package com.ladbrokescoral.oxygen.timeline.api.handlers;

import com.ladbrokescoral.oxygen.timeline.api.channel.ChannelHandlersContext;
import com.ladbrokescoral.oxygen.timeline.api.model.dto.in.LoadPostPageFromInputMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.dto.out.OutputMessageDto;
import com.ladbrokescoral.oxygen.timeline.api.reactive.model.MessageContent;
import com.ladbrokescoral.oxygen.timeline.api.service.LoadNextPageMessageService;
import com.ladbrokescoral.oxygen.timeline.api.service.OnConnectMessageService;
import com.ladbrokescoral.oxygen.timeline.api.ws.model.IncomingRequest;
import com.ladbrokescoral.oxygen.timeline.api.ws.model.IncomingRequestUtil;
import java.time.Duration;
import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.concurrent.ConcurrentHashMap;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.socket.WebSocketHandler;
import org.springframework.web.reactive.socket.WebSocketMessage;
import org.springframework.web.reactive.socket.WebSocketSession;
import reactor.core.publisher.Flux;
import reactor.core.publisher.FluxSink;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

@Component
@Slf4j
@RequiredArgsConstructor
public class TimelineWebsocketHandler implements WebSocketHandler {

  private final OnConnectMessageService onConnectMessageService;
  private final LoadNextPageMessageService loadNextPageMessageService;
  private static final Duration TIMEOUT = Duration.ofSeconds(60);

  @Override
  public Mono<Void> handle(WebSocketSession session) {
    Flux<WebSocketMessage> messagesFlux =
        Flux.create((FluxSink<WebSocketMessage> sink) -> doStartSession(sink, session))
            .doFinally(signalType -> doCleanupSession(session));
    session
        .receive()
        .timeout(
            TIMEOUT, s -> ChannelHandlersContext.wsHandlers.get(session.getId()).closeConnection())
        .subscribe(wsm -> handleIncomingMessages(wsm.getPayloadAsText(), session));

    return session.send(messagesFlux.publishOn(Schedulers.boundedElastic()));
  }

  protected void doStartSession(FluxSink<WebSocketMessage> sink, WebSocketSession session) {
    ReactiveWsMessageHandler messageHandler = createMessageHandler(sink, session);
    ChannelHandlersContext.wsHandlers.put(session.getId(), messageHandler);
    messageHandler.handleMessage(MessageContent.withInitialPayload(session));
    messageHandler.handleMessage(MessageContent.emptyPayloadToClient());
    messageHandler.handleMessage(onConnectMessageService.initialPosts());
    messageHandler.addSubscriptionToAllRooms();
  }

  protected void handleIncomingMessages(String message, WebSocketSession session) {
    try {
      IncomingRequest incomingRequest = IncomingRequestUtil.getIncomingRequest(message);
      ReactiveWsMessageHandler messageHandler =
          ChannelHandlersContext.wsHandlers.get(session.getId());
      switch (incomingRequest.getClientAction()) {
        case PING:
          messageHandler.handleMessage(new MessageContent("3"));
          break;
        case LOAD_POST_PAGE:
          LoadPostPageFromInputMessage inputMessage =
              (LoadPostPageFromInputMessage) createInput(incomingRequest);
          loadNextPageMessageService.onLoadPageEvent(messageHandler, inputMessage);
          break;
        default:
      }
    } catch (Exception e) {
      log.info("Exception handling incoming message {} ", e.getMessage());
    }
  }

  private Object createInput(IncomingRequest request) {
    LoadPostPageFromInputMessage inputMessage = new LoadPostPageFromInputMessage();
    LinkedHashMap<String, String> input =
        (LinkedHashMap) ((LinkedHashMap) request.getInput()).get("from");
    OutputMessageDto.TimeBasedId from =
        new OutputMessageDto.TimeBasedId(
            (String) input.get("id"), Instant.parse((String) input.get("timestamp")));
    inputMessage.setFrom(from);
    return inputMessage;
  }

  protected ReactiveWsMessageHandler createMessageHandler(
      FluxSink<WebSocketMessage> sink, WebSocketSession session) {
    return ReactiveWsMessageHandler.builder()
        .session(session)
        .sink(sink)
        .disposablesOfAllSubscribedChannels(new ConcurrentHashMap<>())
        .build();
  }

  private void doCleanupSession(WebSocketSession session) {
    ReactiveWsMessageHandler handler = ChannelHandlersContext.wsHandlers.remove(session.getId());
    handler.cleanUpCurrentPageContext();
    session.close();
  }
}
