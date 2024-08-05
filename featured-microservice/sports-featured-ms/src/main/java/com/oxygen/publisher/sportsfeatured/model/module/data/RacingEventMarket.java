package com.oxygen.publisher.sportsfeatured.model.module.data;

import java.util.List;
import lombok.Data;

@Data
public class RacingEventMarket {
  private String id;
  private String name;
  private String drilldownTagNames;
  private Integer eachWayFactorNum;
  private Integer eachWayFactorDen;
  private Integer eachWayPlaces;
  private Boolean isEachWayAvailable;
  private Boolean isLpAvailable;
  private Boolean isSpAvailable;
  private Boolean isGpAvailable;
  private Boolean isResulted;
  // OZONE-677 added a newlist to get places field for extrasignplace feature
  private List<ReferenceEachWayTerms> referenceEachWayTerms;
  private String marketStatusCode;
  private String liveServChannels;
  private String liveServChildrenChannels;
}
