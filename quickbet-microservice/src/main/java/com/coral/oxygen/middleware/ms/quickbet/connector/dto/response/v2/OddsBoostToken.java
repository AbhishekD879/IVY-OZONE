package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class OddsBoostToken {
  private String enhancedOddsPrice;
  private String enhancedOddsPriceNum;
  private String enhancedOddsPriceDen;
  private String betBoostMinStake;
  private String betBoostMaxStake;
  private String id;
}
