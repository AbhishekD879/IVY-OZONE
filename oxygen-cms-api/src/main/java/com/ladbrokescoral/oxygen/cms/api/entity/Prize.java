package com.ladbrokescoral.oxygen.cms.api.entity;

import java.math.BigDecimal;
import lombok.Data;

@Data
public class Prize {

  private int correctSelections;
  private PrizeType prizeType;
  private BigDecimal amount;
}
