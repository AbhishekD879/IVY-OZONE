package com.coral.oxygen.edp.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.impl.MessageHandlerMultiplexer;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Envelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.EnvelopeType;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/** Created by azayats on 04.01.18. */
@Component
public class LiveServConnector {

  private final LiveServService liveServService;
  private final MessageHandlerMultiplexer messageMultiplexer;

  private final Map<String, Envelope> lastMessages;

  @Autowired
  public LiveServConnector(
      LiveServService liveServService, MessageHandlerMultiplexer messageMultiplexer) {
    this.liveServService = liveServService;
    this.messageMultiplexer = messageMultiplexer;
    this.lastMessages = new ConcurrentHashMap<>();
    this.messageMultiplexer.addMessageHandler(
        envelope -> {
          if (envelope.getType() == EnvelopeType.UNSUBSCRIBE) {
            lastMessages.remove(envelope.getChannel());
          } else if (envelope.getType() == EnvelopeType.MESSAGE) {
            lastMessages.put(envelope.getChannel(), envelope);
          }
        });
  }

  public void addMessageHandler(MessageHandler messageHandler) {
    this.messageMultiplexer.addMessageHandler(messageHandler);
  }

  public Envelope subscribe(String channel) {
    Envelope result = lastMessages.get(channel);
    liveServService.subscribe(channel);
    return result;
  }

  public void unsubscribe(String channel) {
    liveServService.unsubscribe(channel);
  }
}
