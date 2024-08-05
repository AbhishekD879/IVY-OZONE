package com.ladbrokescoral.oxygen.dto.messages;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ErrorAsk {
  private EnvelopeType type;
  private String channel;
  private String errorMessage;

  public ErrorAsk(String channel) {
    this.type = EnvelopeType.SUBSCRIPTION_ERROR;
    this.channel = channel;
  }
}
