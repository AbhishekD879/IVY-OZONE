package com.coral.oxygen.middleware.ms.liveserv.model.messages;

/** Created by azayats on 08.05.17. */
public abstract class Envelope {

  private final EnvelopeType type;

  private final String channel;

  private final String description;

  public Envelope(EnvelopeType type, String channel, String description) {
    this.type = type;
    this.channel = channel;
    this.description = description;
  }

  public EnvelopeType getType() {
    return type;
  }

  public String getDescription() {
    return description;
  }

  public String getChannel() {
    return channel;
  }

  @Override
  public String toString() {
    final StringBuffer sb = new StringBuffer("Envelope{");
    sb.append("type=").append(type);
    sb.append(", channel='").append(channel).append('\'');
    sb.append(", description='").append(description).append('\'');
    sb.append('}');
    return sb.toString();
  }
}
