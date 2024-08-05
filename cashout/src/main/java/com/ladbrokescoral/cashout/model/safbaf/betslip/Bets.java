package com.ladbrokescoral.cashout.model.safbaf.betslip;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class Bets {
  private List<Bet> bet = new ArrayList<>();
  private Integer numLines;
  private Integer numVoidLines;
  private Integer numWinLines;
  private Integer numLoseLines;
  private List<BetFailure> betFailures = new ArrayList<>();
}
