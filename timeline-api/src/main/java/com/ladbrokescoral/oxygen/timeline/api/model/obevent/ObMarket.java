package com.ladbrokescoral.oxygen.timeline.api.model.obevent;

import java.util.Collections;
import java.util.List;
import lombok.Data;

@Data
public class ObMarket {
  private String id;
  private String eventId;
  private Long templateMarketId;
  private String templateMarketName;
  private String dispSortId;
  private String dispSortName;
  private String collectionIds;
  private String collectionNames;
  private String marketMeaningMajorCode;
  private String marketMeaningMinorCode;
  private String name;
  private String substitutedName;

  private List<ObOutcome> outcomes = Collections.emptyList();

  private Boolean isLpAvailable = false;
  private Boolean isSpAvailable = false;
  private Boolean isGpAvailable = false;
  private Boolean isEachWayAvailable = false;
  private Boolean isPlaceOnlyAvailable = false;
  private Double rawHandicapValue;
  private Integer betInRunIndex;
  private Integer eachWayFactorNum;
  private Integer eachWayFactorDen;
  private Integer eachWayPlaces;
  private Boolean isAntepost;
  private Boolean isResulted;
  private Boolean isMarketBetInRun;
  private Integer displayOrder;
  private String marketStatusCode;
  private Boolean isActive;
  private Boolean isDisplayed;
  private String siteChannels;
  private String liveServChannels;
  private String liveServChildrenChannels;
  private String liveServLastMsgId;
  private String priceTypeCodes;
  private String ncastTypeCodes;
  private Boolean isPoolAvailable;
  private String drilldownTagNames;
  private Boolean isWinAndPlaceAvailable;
  private Boolean isWPPlaceOnlyAvailable;
  private Integer winAndPlacePlaces;
  private Boolean isAvailable;
  private Integer maxAccumulators;
  private Integer minAccumulators;
  private Boolean isStarted;
  private Boolean isCbAvailable;
  private Boolean isFinished;
  private String cashoutAvail;
  private Boolean isRestricted;
  private String flags;

  public void applyMarketUpdate(MarketStatus marketStatus) {
    this.isActive = marketStatus.getActive() != null ? marketStatus.getActive() : this.isActive;
    this.isDisplayed =
        marketStatus.getDisplayed() != null ? marketStatus.getDisplayed() : this.isDisplayed;
    if (marketStatus.getSpAvailable() != null) {
      this.isSpAvailable = marketStatus.getSpAvailable();
      if (!this.isSpAvailable) {
        this.isLpAvailable = true;
      }
    }
    if (marketStatus.getLpAvailable() != null) {
      this.isLpAvailable = marketStatus.getLpAvailable();
    }
    this.priceTypeCodes = "SP, LP";
    // set price type as "SP," if lp is not true.
    if (!this.isLpAvailable) {
      this.priceTypeCodes = "SP,";
    }
    this.isMarketBetInRun =
        marketStatus.getMarketBetInRun() != null
            ? marketStatus.getMarketBetInRun()
            : this.isMarketBetInRun;
    this.marketStatusCode = this.isActive ? "A" : "S";
  }
}
