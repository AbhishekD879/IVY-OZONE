package com.coral.oxygen.middleware.ms.liveserv.model.messages;

import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;

/** Created by azayats on 12.05.17. */
public class MessageEnvelope extends EventMessageEnvelope {

  private final Message message;

  public MessageEnvelope(String channel, long eventId, Message message) {
    super(EnvelopeType.MESSAGE, channel, eventId, null);
    this.message = message;
  }

  public Message getMessage() {
    return message;
  }
}
