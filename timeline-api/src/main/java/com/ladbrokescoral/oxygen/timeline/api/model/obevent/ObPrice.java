package com.ladbrokescoral.oxygen.timeline.api.model.obevent;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Builder
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ObPrice {
  public String id;
  public Boolean isActive;
  public Integer displayOrder;
  public String outcomeVariantId;
  public String priceType;
  public Integer priceNum;
  public Integer priceDen;
  public Double priceDec;
  public String handicapValueDec;
  public Double rawHandicapValue;
  public String poolId;
  public String poolType;
  public Boolean isToPlace;
  private String priceStreamType;
  private Integer priceAmerican;
}
