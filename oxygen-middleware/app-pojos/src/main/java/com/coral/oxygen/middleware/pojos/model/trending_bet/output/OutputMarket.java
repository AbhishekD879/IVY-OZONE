package com.coral.oxygen.middleware.pojos.model.trending_bet.output;

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
  private String marketStatusCode;
  private Boolean isActive;
  private Boolean isDisplayed;
  private Long templateMarketId;
  private String templateMarketName;
  private String drilldownTagNames;

  private List<OutputOutcome> outcomes;
}
