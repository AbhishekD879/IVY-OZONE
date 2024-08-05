package com.ladbrokescoral.cashout.model.safbaf.betslip;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class Promotion {
  private String promotionToken;
  private String promotionName;
  private Double rewardValue;
  private String promotionExpiryDateTime;
  private List<PromotionRestriction> promotionRestrictions = new ArrayList<>();
}
