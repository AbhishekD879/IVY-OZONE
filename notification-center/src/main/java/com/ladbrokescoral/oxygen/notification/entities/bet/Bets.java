package com.ladbrokescoral.oxygen.notification.entities.bet;

import java.util.ArrayList;
import lombok.Data;

@Data
public class Bets {
  private ArrayList<Bet> bet;
  private Integer numLines;
  private Integer numVoidLines;
  private Integer numWinLines;
  private Integer numLoseLines;
  private ArrayList<BetFailure> betFailures;
}
