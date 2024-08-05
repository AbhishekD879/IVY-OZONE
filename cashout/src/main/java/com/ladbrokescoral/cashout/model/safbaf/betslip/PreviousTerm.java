package com.ladbrokescoral.cashout.model.safbaf.betslip;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class PreviousTerm {
  private String reason;

  @JsonProperty("previousTermPrice")
  private Price previousTermPrice;
}
