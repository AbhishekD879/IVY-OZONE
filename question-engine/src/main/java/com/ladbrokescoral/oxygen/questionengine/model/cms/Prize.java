package com.ladbrokescoral.oxygen.questionengine.model.cms;

import java.math.BigDecimal;
import lombok.Data;

@Data
public class Prize {
  private PrizeType prizeType;
  private BigDecimal amount;
  private String currency;
  private String promotionId;
}
