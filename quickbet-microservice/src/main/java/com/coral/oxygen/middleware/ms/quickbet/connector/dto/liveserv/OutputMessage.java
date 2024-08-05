package com.coral.oxygen.middleware.ms.quickbet.connector.dto.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.model.messages.EnvelopeType;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class OutputMessage {
  private EnvelopeType type;
  private OutputEvent event;
  private OutputChannel channel;
  private OutputChannel subChannel;
  private Object message;

  public OutputMessage withType(EnvelopeType type) {
    this.type = type;
    return this;
  }

  public OutputMessage withEvent(OutputEvent event) {
    this.event = event;
    return this;
  }

  public OutputMessage withChannel(OutputChannel channel) {
    this.channel = channel;
    return this;
  }

  public OutputMessage withSubChannel(OutputChannel subChannel) {
    this.subChannel = subChannel;
    return this;
  }

  public OutputMessage withMessage(Object message) {
    this.message = message;
    return this;
  }
}
