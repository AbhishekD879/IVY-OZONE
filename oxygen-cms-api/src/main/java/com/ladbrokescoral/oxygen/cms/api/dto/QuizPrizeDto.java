package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PrizeType;
import java.math.BigDecimal;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class QuizPrizeDto {
  private PrizeType prizeType;
  private BigDecimal amount;
  private String currency;
  private String promotionId;
}