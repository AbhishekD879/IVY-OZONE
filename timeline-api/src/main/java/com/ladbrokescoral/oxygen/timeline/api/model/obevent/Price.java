package com.ladbrokescoral.oxygen.timeline.api.model.obevent;

import java.math.BigDecimal;
import lombok.Data;

@Data
public class Price {

  private int priceNum;
  private int priceDen;
  private BigDecimal price;
  private Boolean startPrice;
}
