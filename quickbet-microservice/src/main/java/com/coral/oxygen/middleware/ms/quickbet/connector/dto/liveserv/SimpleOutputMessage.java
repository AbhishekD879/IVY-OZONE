package com.coral.oxygen.middleware.ms.quickbet.connector.dto.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.model.messages.EnvelopeType;

public class SimpleOutputMessage {
  private EnvelopeType type;
  private String channel;
  private String description;

  public SimpleOutputMessage() {}

  public SimpleOutputMessage(EnvelopeType type, String channel, String description) {
    this.type = type;
    this.channel = channel;
    this.description = description;
  }

  public EnvelopeType getType() {
    return type;
  }

  public String getChannel() {
    return channel;
  }

  public String getDescription() {
    return description;
  }

  public void setType(EnvelopeType type) {
    this.type = type;
  }

  public void setChannel(String channel) {
    this.channel = channel;
  }

  public void setDescription(String description) {
    this.description = description;
  }
}
