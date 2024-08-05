package com.ladbrokescoral.oxygen.trendingbets.model;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode
public class OutputPrice {

  protected String id;
  protected String priceType;
  protected Integer priceNum;
  protected Integer priceDen;
  protected Double priceDec;
  protected String handicapValueDec;
  protected Double rawHandicapValue;
  protected String priceStreamType;
  protected Integer priceAmerican;
  private Boolean isActive;
}
