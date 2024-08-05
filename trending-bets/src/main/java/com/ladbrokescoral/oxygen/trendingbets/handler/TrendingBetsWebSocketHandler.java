package com.ladbrokescoral.oxygen.trendingbets.handler;

import com.ladbrokescoral.oxygen.trendingbets.context.ChannelHandlersContext;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.model.IncomingRequest;
import com.ladbrokescoral.oxygen.trendingbets.model.MessageContent;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingBetsDto;
import com.ladbrokescoral.oxygen.trendingbets.util.IncomingRequestUtil;
import java.time.Duration;
import lombok.AllArgsConstructor;
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
@AllArgsConstructor
@Slf4j
public class TrendingBetsWebSocketHandler implements WebSocketHandler {

  private static final Duration TIMEOUT = Duration.ofSeconds(60);

  @Override
  public Mono<Void> handle(WebSocketSession session) {
    Flux<WebSocketMessage> messagesFlux =
        Flux.create((FluxSink<WebSocketMessage> sink) -> doStartSession(sink, session))
            .doFinally(signalType -> doCleanupSession(session));
    session
        .receive()
        .timeout(
            TIMEOUT,
            s -> ChannelHandlersContext.getWsHandlers().get(session.getId()).closeConnection())
        .subscribe(wsm -> handleIncomingMessages(wsm.getPayloadAsText(), session));
    return session.send(messagesFlux.publishOn(Schedulers.boundedElastic()));
  }

  protected ReactiveWsMessageHandler createMessageHandler(
      FluxSink<WebSocketMessage> sink, WebSocketSession session) {
    return ReactiveWsMessageHandler.builder().session(session).sink(sink).build();
  }

  protected void doStartSession(FluxSink<WebSocketMessage> sink, WebSocketSession session) {
    ReactiveWsMessageHandler messageHandler = createMessageHandler(sink, session);
    ChannelHandlersContext.getWsHandlers().put(session.getId(), messageHandler);
    messageHandler.handleMessage(MessageContent.withInitialPayload(session.getId()));
  }

  protected void handleIncomingMessages(String message, WebSocketSession session) {
    try {
      IncomingRequest incomingRequest = IncomingRequestUtil.getIncomingRequest(message);
      ReactiveWsMessageHandler messageHandler =
          ChannelHandlersContext.getWsHandlers().get(session.getId());
      switch (incomingRequest.clientAction()) {
        case SUBSCRIBE -> processSubscribeRequest(incomingRequest, messageHandler);
        case PING -> messageHandler.handleMessage(new MessageContent("3"));
        case DISCONNECT -> messageHandler.closeConnection();
        default -> log.error("Invalid client action in websocket");
      }
    } catch (Exception e) {
      log.error("Exception handling incoming message", e);
    }
  }

  private void processSubscribeRequest(
      IncomingRequest incomingRequest, ReactiveWsMessageHandler messageHandler) {
    if (incomingRequest.input() != null) {
      String channelId = incomingRequest.input().toString();
      TrendingBetsDto trendingBetsDto = TrendingBetsContext.getTrendingBets().get(channelId);
      if (trendingBetsDto != null) {
        messageHandler.handleMessage(MessageContent.withPayload(channelId, trendingBetsDto));
        messageHandler.subscribe(channelId);
      } else {
        messageHandler.handleMessage(MessageContent.withPayload(channelId, "INVALID CHANNEL"));
      }
    }
  }

  private void doCleanupSession(WebSocketSession session) {
    ReactiveWsMessageHandler handler =
        ChannelHandlersContext.getWsHandlers().remove(session.getId());
    handler.cleanUpContext();
    session.close();
  }
}
