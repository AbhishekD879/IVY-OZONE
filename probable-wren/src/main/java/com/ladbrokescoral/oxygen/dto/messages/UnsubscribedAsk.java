package com.ladbrokescoral.oxygen.dto.messages;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class UnsubscribedAsk {
  private EnvelopeType type;
  private String channel;

  public UnsubscribedAsk(String channel) {
    this.type = EnvelopeType.UNSUBSCRIBE;
    this.channel = channel;
  }
}
