package com.ladbrokescoral.oxygen.questionengine.dto.cms;

import com.ladbrokescoral.oxygen.questionengine.model.cms.PrizeType;
import java.math.BigDecimal;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class PrizeDto {
  private PrizeType prizeType;
  private BigDecimal amount;
  private String currency;
  private String promotionId;
}
