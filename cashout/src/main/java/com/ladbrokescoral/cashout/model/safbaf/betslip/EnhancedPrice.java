package com.ladbrokescoral.cashout.model.safbaf.betslip;

import java.math.BigInteger;
import lombok.Data;

@Data
public class EnhancedPrice {
  private String priceType;
  private String priceStatus;
  private Integer num;
  private Integer den;
  private Boolean isEarlyPrice;
  private Double decimalPrice;
  private String token;
  private BigInteger selectionKey;
}
