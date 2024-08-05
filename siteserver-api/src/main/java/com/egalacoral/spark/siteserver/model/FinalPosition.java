package com.egalacoral.spark.siteserver.model;

import lombok.Data;

@Data
public class FinalPosition {
  private String id;
  private String outcomeId;
  private String marketId;
  private String siteChannels;
  private Integer position;
  private String name;
  private Integer runnerNumber;
  private String startingPriceNum;
  private String startingPriceDen;
  private String startingPriceDec;
}
