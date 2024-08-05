package com.coral.oxygen.middleware.ms.liveserv.model.messages;

/** Created by azayats on 08.05.17. */
public class Unsubscribed extends EventMessageEnvelope {

  public Unsubscribed(String channel, long eventId) {
    super(EnvelopeType.UNSUBSCRIBE, channel, eventId, null);
  }
}
