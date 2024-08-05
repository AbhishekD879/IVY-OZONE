package com.ladbrokescoral.oxygen.trendingbets.model;

import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode
public class OutputMarket {

  private String id;
  private String name;
  private Boolean isLpAvailable;
  private Boolean isSpAvailable;
  private Boolean isGpAvailable;
  private Double rawHandicapValue;
  private String liveServChannels;
  private String liveServChildrenChannels;
  private String marketStatusCode;
  private Boolean isActive;
  private Boolean isDisplayed;
  private Long templateMarketId;
  private String templateMarketName;
  private String drilldownTagNames;
  private int minAccumulators;
  private int maxAccumulators;

  private List<OutputOutcome> outcomes;
}
