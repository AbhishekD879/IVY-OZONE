package com.ladbrokescoral.oxygen.cms.api.entity;

import java.math.BigDecimal;
import javax.annotation.Nullable;
import lombok.Data;
import lombok.experimental.Accessors;

/** UI sends empty Price object (with all null values), when no price is specified */
@Data
@Accessors(chain = true)
public class Price {
  @Nullable private String priceType;
  @Nullable private Integer priceNum;
  @Nullable private Integer priceDen;
  @Nullable private BigDecimal priceDec;
}
