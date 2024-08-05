package com.ladbrokescoral.cashout.model.safbaf.betslip;

import lombok.Data;

@Data
public class PromotionRestriction {
  private String restrictionValue;
  private String restrictionType;
  private String betType;
  private String betId;
}
