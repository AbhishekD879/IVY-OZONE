package com.coral.oxygen.middleware.ms.liveserv.impl;

import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.EventMessageEnvelope;
import com.newrelic.api.agent.Trace;
import java.util.ArrayList;
import java.util.List;
import lombok.extern.slf4j.Slf4j;

/** Created by azayats on 08.05.17. */
@Slf4j
public class MessageHandlerMultiplexer implements MessageHandler {

  private List<MessageHandler> handlers = new ArrayList<>();

  @Trace(metricName = "AddMessageHandler")
  public void addMessageHandler(MessageHandler messageHandler) {
    List<MessageHandler> newHandlers = new ArrayList<>(this.handlers.size() + 1);
    newHandlers.addAll(this.handlers);
    newHandlers.add(messageHandler);
    this.handlers = newHandlers;
  }

  @Trace(metricName = "OnMessage")
  @Override
  public void handle(EventMessageEnvelope envelope) {
    handlers.forEach(
        handler -> {
          log.trace("Handler {} try to process {}", handler, envelope);
          handler.handle(envelope);
        });
  }
}
