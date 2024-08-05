package com.coral.oxygen.middleware.pojos.model.output;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import java.io.Serializable;
import java.util.List;
import lombok.Data;

@Data
public class RacingEventMarket implements Serializable {
  private String id;
  private String name;
  private String drilldownTagNames;
  private Integer eachWayFactorNum;
  private Integer eachWayFactorDen;
  private Integer eachWayPlaces;
  private Boolean isEachWayAvailable;
  private Boolean isLpAvailable;
  private Boolean isSpAvailable;
  // add gp(guaranteed price)
  private Boolean isGpAvailable;

  private Boolean isResulted;
  // add ReferenceEachWayTerms for extrasign place posting
  private List<ReferenceEachWayTerms> referenceEachWayTerms;
  private String effectiveGpStartTime;
  private String marketStatusCode;
  private String liveServChannels;
  private String liveServChildrenChannels;

  @ChangeDetect(minor = true)
  public String getMarketStatusCode() {
    return marketStatusCode;
  }

  @ChangeDetect
  public Boolean getIsLpAvailable() {
    return isLpAvailable;
  }

  @ChangeDetect(minor = true)
  public Boolean getResulted() {
    return isResulted;
  }
}
