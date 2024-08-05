package com.ladbrokescoral.cashout.payout;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class PotentialReturns {
  @JsonProperty("betNo")
  private String betId;

  private double returns;
}
