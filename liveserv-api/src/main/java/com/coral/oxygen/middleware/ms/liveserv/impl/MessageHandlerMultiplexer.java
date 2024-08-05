package com.coral.oxygen.middleware.ms.liveserv.impl;

import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Envelope;
import java.util.ArrayList;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/** Created by azayats on 08.05.17. */
public class MessageHandlerMultiplexer implements MessageHandler {

  private static final transient Logger LOGGER =
      LoggerFactory.getLogger(MessageHandlerMultiplexer.class);

  private List<MessageHandler> handlers = new ArrayList<>();

  public void addMessageHandler(MessageHandler messageHandler) {
    List<MessageHandler> newHandlers = new ArrayList<>(this.handlers.size() + 1);
    newHandlers.addAll(this.handlers);
    newHandlers.add(messageHandler);
    this.handlers = newHandlers;
  }

  @Override
  public void handle(Envelope envelope) {
    handlers
        .parallelStream()
        .forEach(
            handler -> {
              try {
                handler.handle(envelope);
              } catch (Exception e) {
                LOGGER.error("Handling of message {} failed by {}", envelope, handler, e);
              }
            });
  }
}
