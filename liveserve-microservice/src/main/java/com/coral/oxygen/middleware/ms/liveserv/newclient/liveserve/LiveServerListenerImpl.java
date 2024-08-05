package com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve;

import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.coral.oxygen.middleware.ms.liveserv.newclient.EventIdResolver;
import com.newrelic.api.agent.NewRelic;
import java.util.List;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class LiveServerListenerImpl implements LiveServerListener {
  private static final int MESSAGE_KEY_END_INDEX = 17;
  private final MessageHandler messageHandler;
  private final EventIdResolver eventIdResolver;

  public LiveServerListenerImpl(MessageHandler messageHandler, EventIdResolver eventIdResolver) {
    this.messageHandler = messageHandler;
    this.eventIdResolver = eventIdResolver;
  }

  @Override
  public void onMessage(List<Message> messages) {
    messages.parallelStream().forEach(this::processMessage);
  }

  @Override
  public void onError(Throwable e) {
    log.error("onError called.", e);
  }

  private void processMessage(Message message) {
    String channel = message.getMessageCode().substring(1, MESSAGE_KEY_END_INDEX);
    eventIdResolver
        .resolveEventId(channel)
        .map(
            eventId -> {
              messageHandler.handle(new MessageEnvelope(channel, eventId, message));
              return eventId;
            })
        .orElseGet(
            () -> {
              String errorMessage = "Couldn't resolve event id for channel=" + channel;
              log.error(errorMessage);
              NewRelic.noticeError(errorMessage);
              return null;
            });
  }
}
