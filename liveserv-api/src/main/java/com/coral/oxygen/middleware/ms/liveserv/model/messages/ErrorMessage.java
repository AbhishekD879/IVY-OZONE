package com.coral.oxygen.middleware.ms.liveserv.model.messages;

/** Created by azayats on 10.05.17. */
public class ErrorMessage extends AbstractErrorEnvelope {

  private final Long eventId;

  public ErrorMessage(String channel, Long eventId, String description) {
    super(EnvelopeType.ERROR, channel, description);
    this.eventId = eventId;
  }

  public ErrorMessage(String channel, Long eventId, String description, Throwable e) {
    super(EnvelopeType.ERROR, channel, description, e);
    this.eventId = eventId;
  }

  public Long getEventId() {
    return eventId;
  }
}
