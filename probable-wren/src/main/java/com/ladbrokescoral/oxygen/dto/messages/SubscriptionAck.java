package com.ladbrokescoral.oxygen.dto.messages;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SubscriptionAck {
  private EnvelopeType type;
  private String channel;

  public SubscriptionAck(String channel) {
    this.type = EnvelopeType.SUBSCRIBED;
    this.channel = channel;
  }
}
