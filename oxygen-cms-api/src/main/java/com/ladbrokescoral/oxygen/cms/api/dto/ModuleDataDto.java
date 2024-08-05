package com.ladbrokescoral.oxygen.cms.api.dto;

import java.math.BigInteger;
import lombok.Data;

@Data
public class ModuleDataDto {
  private Integer marketsCount;
  private BigInteger outcomeId;
  private String marketId;
  private boolean outcomeStatus;
  private boolean outright;
  private String name;
  private String categoryId;
  private String id;
  private String nameOverride;
}
