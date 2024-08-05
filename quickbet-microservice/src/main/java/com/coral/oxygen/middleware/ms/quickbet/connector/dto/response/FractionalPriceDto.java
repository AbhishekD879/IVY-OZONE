package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response;

import lombok.Data;
import lombok.RequiredArgsConstructor;

@Data
@RequiredArgsConstructor
public class FractionalPriceDto {
  private final Integer priceNum;
  private final Integer priceDen;
}
