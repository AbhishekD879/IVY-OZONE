package com.egalacoral.spark.siteserver.model;

import lombok.Data;

@Data
public class NcastDividend {

  private String id;
  private String marketId;
  private String siteChannels;
  private String type;
  private String dividend;
  private String runnerNumbers;
}
