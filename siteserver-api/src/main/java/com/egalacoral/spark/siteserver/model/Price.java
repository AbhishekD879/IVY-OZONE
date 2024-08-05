package com.egalacoral.spark.siteserver.model;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class Price extends Identity {

  private String id;
  private Boolean isActive;
  private Integer displayOrder;
  private String outcomeVariantId;
  private String priceType;
  private Integer priceNum;
  private Integer priceDen;
  private Double priceDec;
  private String handicapValueDec;
  private Double rawHandicapValue;
  private String poolId;
  private String poolType;
  private Boolean isToPlace;
  private String priceStreamType;
  private Integer priceAmerican;
}
