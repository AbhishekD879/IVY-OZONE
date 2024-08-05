package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public final class OutputPrice {
  private String id;
  private String priceType;
  private Integer priceNum;
  private Integer priceDen;
  private Double priceDec;
  private String handicapValueDec;
  private Double rawHandicapValue;
  private String priceStreamType;
  private Integer priceAmerican;
}
