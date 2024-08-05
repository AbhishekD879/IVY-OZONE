package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class PriceDto {
  private String priceNum;
  private String priceDen;
  private IdRefDto priceTypeRef;

  public PriceDto(String priceNum, String priceDen, String id) {
    this.priceNum = priceNum;
    this.priceDen = priceDen;
    this.priceTypeRef = new IdRefDto(id);
  }
}
