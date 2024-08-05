package com.coral.oxygen.middleware.ms.liveserv.model.messages;

/** Created by azayats on 10.05.17. */
public abstract class EventMessageEnvelope extends Envelope {

  private final long eventId;

  public EventMessageEnvelope(EnvelopeType type, String channel, long eventId, String description) {
    super(type, channel, description);
    this.eventId = eventId;
  }

  public long getEventId() {
    return eventId;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("EventMessageEnvelope{");
    sb.append("super=").append(super.toString());
    sb.append(", eventId=").append(eventId);
    sb.append('}');
    return sb.toString();
  }
}
