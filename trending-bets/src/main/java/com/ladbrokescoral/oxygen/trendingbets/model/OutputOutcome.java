package com.ladbrokescoral.oxygen.trendingbets.model;

import java.util.List;
import lombok.Data;

@Data
public class OutputOutcome {

  protected String id;
  protected String name;
  protected String liveServChannels;
  private String liveServChildrenChannels;
  private List<OutputPrice> prices;
  private String outcomeMeaningMajorCode;
  private String outcomeStatusCode;
  private String marketId;
  private Boolean isActive;
  private Boolean isDisplayed;
  private String drilldownTagNames;
}
