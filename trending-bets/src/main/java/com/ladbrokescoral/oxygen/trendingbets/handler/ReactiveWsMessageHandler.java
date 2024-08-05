package com.ladbrokescoral.oxygen.trendingbets.handler;

import com.ladbrokescoral.oxygen.trendingbets.context.ChannelHandlersContext;
import lombok.Builder;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessagingException;
import org.springframework.web.reactive.socket.WebSocketMessage;
import org.springframework.web.reactive.socket.WebSocketSession;
import reactor.core.Disposable;
import reactor.core.publisher.FluxSink;
import reactor.core.publisher.Sinks;
import reactor.core.scheduler.Schedulers;

/**
 * ForwardingMessageHandler is a one to one map with the WebSocket Session, which holds the sink
 * responsible to publish the message to client. Also, keeps track of all the subscriptions made to
 * page, module and events flux.
 */
@Builder
@Data
@Slf4j
public class ReactiveWsMessageHandler {
  private WebSocketSession session;
  private FluxSink<WebSocketMessage> sink;

  private Disposable subscriber;

  /**
   * publishes the message to client through sink created for the respective WebSocket Session
   *
   * @param message
   * @throws MessagingException
   */
  public void handleMessage(Message<String> message) throws MessagingException {
    WebSocketMessage webSocketMessage = session.textMessage(message.getPayload());
    sink.next(webSocketMessage);
  }

  public void closeConnection() {
    sink.complete();
  }

  public void cleanUpContext() {
    if (subscriber != null) {
      subscriber.dispose();
      subscriber = null;
    }
  }

  /**
   * Subscribes to the given channel.
   *
   * @param channelId
   */
  public void subscribe(String channelId) {
    subscribe(ChannelHandlersContext.createIfAbsentAndReturnChannel(channelId), channelId);
  }

  /**
   * Subscribes to the given channel. Previous subscription will be cleared.
   *
   * @param channel
   * @param channelId
   */
  public void subscribe(Sinks.Many<Message<String>> channel, String channelId) {
    cleanUpContext();
    subscriber =
        channel
            .asFlux()
            .publishOn(Schedulers.boundedElastic())
            .subscribe(
                this::handleMessage,
                (Throwable throwable) ->
                    log.error("Error occurred for :: {}", channelId, throwable));
  }
}
