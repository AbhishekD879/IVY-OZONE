package com.coral.oxygen.middleware.ms.liveserv.model.messages;

/** Created by azayats on 08.05.17. */
public class SubscriptionAck extends EventMessageEnvelope {

  public SubscriptionAck(String channel, long eventId) {
    super(EnvelopeType.SUBSCRIBED, channel, eventId, null);
  }
}
