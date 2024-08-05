package com.ladbrokescoral.oxygen.timeline.api.handlers;

import com.ladbrokescoral.oxygen.timeline.api.channel.ChannelHandlersContext;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
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

@Builder
@Data
@Slf4j
public class ReactiveWsMessageHandler {
  private WebSocketSession session;
  private FluxSink<WebSocketMessage> sink;
  private Map<String, Disposable> disposablesOfAllSubscribedChannels;

  public void handleMessage(Message<?> message) throws MessagingException {
    WebSocketMessage webSocketMessage = session.textMessage(message.getPayload().toString());
    sink.next(webSocketMessage);
  }

  public void addSubscriptionToAllRooms() {
    Map<String, List<Sinks.Many<Message<?>>>> channels = ChannelHandlersContext.channels;
    channels.forEach(
        (String key, List<Sinks.Many<Message<?>>> list) -> {
          Sinks.Many<Message<?>> first = list.stream().findFirst().get();
          Disposable subscribe =
              first
                  .asFlux()
                  .publishOn(Schedulers.boundedElastic())
                  .subscribe(
                      this::handleMessage,
                      throwable -> log.error("Error occurred for :: {} {}", throwable, key));
          disposablesOfAllSubscribedChannels.put(key, subscribe);
          ChannelHandlersContext.messageHandlersPerPage
              .computeIfAbsent(key, (keys) -> new HashSet<>())
              .add(this);
        });
  }

  public void cleanUpCurrentPageContext() {
    disposablesOfAllSubscribedChannels.forEach(
        (channelId, disposable) -> disposeAndRemove(disposable, channelId));
    disposablesOfAllSubscribedChannels.clear();
  }

  private void disposeAndRemove(Disposable disposable, String channelId) {
    if (disposable != null) {
      disposable.dispose();
      ChannelHandlersContext.messageHandlersPerPage.get(channelId).remove(this);
    }
  }

  public void closeConnection() {
    sink.complete();
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    ReactiveWsMessageHandler that = (ReactiveWsMessageHandler) o;
    return session.equals(that.session);
  }

  @Override
  public int hashCode() {
    return Objects.hash(session);
  }
}
