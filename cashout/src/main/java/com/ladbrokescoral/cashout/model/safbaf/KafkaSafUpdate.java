package com.ladbrokescoral.cashout.model.safbaf;

import lombok.Data;

@Data
public class KafkaSafUpdate {
  private Event event;
  private Market market;
  private Selection selection;
}
