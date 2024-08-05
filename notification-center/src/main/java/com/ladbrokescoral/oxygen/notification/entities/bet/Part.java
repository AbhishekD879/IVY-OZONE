package com.ladbrokescoral.oxygen.notification.entities.bet;

import lombok.Data;

@Data
public class Part {
  private BetPrice betPrice;
  private String rawHandicapValue;
  private String selectionKey;
  private String marketKey;
  private String eventKey;
  private String handicapValue;
  private String winPlace;
  private boolean isInRunning;
}
