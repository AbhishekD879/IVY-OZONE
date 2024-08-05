package com.ladbrokescoral.oxygen.cms.api.dto;

import java.math.BigDecimal;
import javax.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Builder
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PriceDto {
  @NotNull private String priceType;
  @NotNull private Integer priceNum;
  @NotNull private Integer priceDen;
  @NotNull private BigDecimal priceDec;
  private String priceStreamType;
  private Integer priceAmerican;
}
