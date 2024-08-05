package com.ladbrokescoral.oxygen.notification.entities.bet;

import lombok.Data;

@Data
public class BetPrice {
  private String priceType;
  private int num;
  private int den;
  private boolean isEarlyPrice;
  private double decimalPrice;
}
