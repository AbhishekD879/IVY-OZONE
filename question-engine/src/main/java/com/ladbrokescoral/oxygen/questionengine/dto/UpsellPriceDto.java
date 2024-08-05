package com.ladbrokescoral.oxygen.questionengine.dto;

import lombok.Data;
import lombok.experimental.Accessors;

import java.math.BigDecimal;

@Data
@Accessors(chain = true)
public class UpsellPriceDto {
  private long selectionId;
  private BigDecimal price;
  private Integer priceNum;
  private Integer priceDen;
  private String selectionName;
  private String marketName;
}
