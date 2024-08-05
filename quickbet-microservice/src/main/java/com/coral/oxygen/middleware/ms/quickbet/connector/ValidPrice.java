package com.coral.oxygen.middleware.ms.quickbet.connector;

/** Created by JacksonGenerator on 5/4/18. */
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ValidPrice {
  private Integer priceNum;
  private Integer priceDen;
}
