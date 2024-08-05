package com.ladbrokescoral.oxygen.cms.api.entity.questionengine;

import com.ladbrokescoral.oxygen.cms.api.entity.PrizeType;
import java.math.BigDecimal;
import lombok.Data;

@Data
public class QuizPrize {

  private int correctSelections;
  private PrizeType prizeType;
  private BigDecimal amount;
  private String currency;
  private String promotionId;
}
