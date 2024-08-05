package com.egalacoral.spark.siteserver.model;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class Pool extends Identity {

  private String id;
  private String provider;
  private String type;
  private String currencyCode;
  private String marketIds;
  private String legCount;
  private String poolValue;
  private String isActive;
  private String minTotalStake;
  private String maxTotalStake;
  private String minStakePerLine;
  private String maxStakePerLine;
  private String stakeIncrementFactor;
}
