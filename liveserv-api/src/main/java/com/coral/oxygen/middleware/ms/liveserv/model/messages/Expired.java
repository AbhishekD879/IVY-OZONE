package com.coral.oxygen.middleware.ms.liveserv.model.messages;

public class Expired extends EventMessageEnvelope {

  public Expired(String channel, long eventId) {
    super(EnvelopeType.EXPIRED, channel, eventId, null);
  }
}
