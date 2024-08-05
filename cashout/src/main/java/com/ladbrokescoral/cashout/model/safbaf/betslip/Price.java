package com.ladbrokescoral.cashout.model.safbaf.betslip;

import lombok.Data;

@Data
public class Price {
  private String priceType;
  private String priceStatus;
  private Integer num;
  private Integer den;
  private Boolean isEarlyPrice;
  private Double decimalPrice;
}
