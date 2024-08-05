package com.entain.oxygen.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class PriceDto {

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
