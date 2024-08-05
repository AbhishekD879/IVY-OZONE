package com.coral.siteserver.model;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public class Market extends Identity implements Serializable {

  private static final long serialVersionUID = 3573137958141281659L;

  protected List<Children> children;
  protected String id;
  protected String eventId;
  protected Long templateMarketId;
  protected String templateMarketName;
  protected String dispSortId;
  protected String dispSortName;
  protected String collectionIds;
  protected String collectionNames;
  protected String marketMeaningMajorCode;
  protected String marketMeaningMinorCode;
  protected String name;
  protected String substitutedName;
  protected Boolean isLpAvailable = false;
  protected Boolean isSpAvailable = false;
  protected Boolean isGpAvailable = false;
  protected Boolean isEachWayAvailable = false;
  protected Boolean isPlaceOnlyAvailable = false;
  protected Double rawHandicapValue;
  protected Integer betInRunIndex;
  protected Integer eachWayFactorNum;
  protected Integer eachWayFactorDen;
  protected Integer eachWayPlaces;
  protected Boolean isAntepost;
  protected Boolean isResulted;
  protected Boolean isMarketBetInRun;
  protected Integer displayOrder;
  protected String marketStatusCode;
  protected Boolean isActive;
  protected Boolean isDisplayed;
  protected String flags;
  protected String siteChannels;
  protected String liveServChannels;
  protected String liveServChildrenChannels;
  protected String liveServLastMsgId;
  protected String priceTypeCodes;
  protected String ncastTypeCodes;
  protected Boolean isPoolAvailable;
  protected String drilldownTagNames;
  protected Boolean isWinAndPlaceAvailable;
  protected Boolean isWPPlaceOnlyAvailable;
  protected Integer winAndPlacePlaces;
  protected Boolean isAvailable;
  protected Integer maxAccumulators;
  protected Boolean isStarted;
  protected Boolean isCbAvailable;
  protected Boolean isFinished;
  protected String cashoutAvail;
  protected Boolean isRestricted;

  private List<Children> getChildren() {
    if (children == null) return new ArrayList<>();
    return children;
  }

  public List<Outcome> getOutcomes() {
    return this.getChildren().stream()
        .map(Children::getOutcome)
        .filter(Objects::nonNull)
        .collect(Collectors.toList());
  }

  public String getId() {
    return id;
  }

  public String getEventId() {
    return eventId;
  }

  public Long getTemplateMarketId() {
    return templateMarketId;
  }

  public String getTemplateMarketName() {
    return templateMarketName;
  }

  public String getDispSortId() {
    return dispSortId;
  }

  public String getDispSortName() {
    return dispSortName;
  }

  public String getCollectionIds() {
    return collectionIds;
  }

  public String getCollectionNames() {
    return collectionNames;
  }

  public String getMarketMeaningMajorCode() {
    return marketMeaningMajorCode;
  }

  public String getMarketMeaningMinorCode() {
    return marketMeaningMinorCode;
  }

  public String getName() {
    return name;
  }

  public String getSubstitutedName() {
    return substitutedName;
  }

  public Boolean getLpAvailable() {
    return isLpAvailable;
  }

  public Boolean getSpAvailable() {
    return isSpAvailable;
  }

  public Boolean getGpAvailable() {
    return isGpAvailable;
  }

  public Boolean getEachWayAvailable() {
    return isEachWayAvailable;
  }

  public Boolean getPlaceOnlyAvailable() {
    return isPlaceOnlyAvailable;
  }

  public Double getRawHandicapValue() {
    return rawHandicapValue;
  }

  public Integer getBetInRunIndex() {
    return betInRunIndex;
  }

  public Integer getEachWayFactorNum() {
    return eachWayFactorNum;
  }

  public Integer getEachWayFactorDen() {
    return eachWayFactorDen;
  }

  public Integer getEachWayPlaces() {
    return eachWayPlaces;
  }

  public Boolean getAntepost() {
    return isAntepost;
  }

  public Boolean getResulted() {
    return isResulted;
  }

  public Boolean getMarketBetInRun() {
    return isMarketBetInRun;
  }

  public Integer getDisplayOrder() {
    return displayOrder;
  }

  public String getMarketStatusCode() {
    return marketStatusCode;
  }

  public Boolean getActive() {
    return isActive;
  }

  public Boolean getDisplayed() {
    return isDisplayed;
  }

  public String getFlags() {
    return flags;
  }

  public String getSiteChannels() {
    return siteChannels;
  }

  public String getLiveServChannels() {
    return liveServChannels;
  }

  public String getLiveServChildrenChannels() {
    return liveServChildrenChannels;
  }

  public String getLiveServLastMsgId() {
    return liveServLastMsgId;
  }

  public String getPriceTypeCodes() {
    return priceTypeCodes;
  }

  public String getNcastTypeCodes() {
    return ncastTypeCodes;
  }

  public Boolean getPoolAvailable() {
    return isPoolAvailable;
  }

  public String getDrilldownTagNames() {
    return drilldownTagNames;
  }

  public Boolean getWinAndPlaceAvailable() {
    return isWinAndPlaceAvailable;
  }

  public Boolean getWPPlaceOnlyAvailable() {
    return isWPPlaceOnlyAvailable;
  }

  public Integer getWinAndPlacePlaces() {
    return winAndPlacePlaces;
  }

  public Boolean getAvailable() {
    return isAvailable;
  }

  public Integer getMaxAccumulators() {
    return maxAccumulators;
  }

  public Boolean getStarted() {
    return isStarted;
  }

  public Boolean getCbAvailable() {
    return isCbAvailable;
  }

  public Boolean getFinished() {
    return isFinished;
  }

  public String getCashoutAvail() {
    return cashoutAvail;
  }

  public Boolean getRestricted() {
    return isRestricted;
  }

  @Override
  public String toString() {
    return super.toString()
        + ", id='"
        + id
        + '\''
        + ", eventId='"
        + eventId
        + '\''
        + ", templateMarketId='"
        + templateMarketId
        + '\''
        + ", templateMarketName='"
        + templateMarketName
        + '\''
        + ", dispSortId='"
        + dispSortId
        + '\''
        + ", dispSortName='"
        + dispSortName
        + '\''
        + ", collectionIds='"
        + collectionIds
        + '\''
        + ", collectionNames='"
        + collectionNames
        + '\''
        + ", marketMeaningMajorCode='"
        + marketMeaningMajorCode
        + '\''
        + ", marketMeaningMinorCode='"
        + marketMeaningMinorCode
        + '\''
        + ", name='"
        + name
        + '\''
        + ", substitutedName='"
        + substitutedName
        + '\''
        + ", isLpAvailable="
        + isLpAvailable
        + ", isSpAvailable="
        + isSpAvailable
        + ", isGpAvailable="
        + isGpAvailable
        + ", isEachWayAvailable="
        + isEachWayAvailable
        + ", isPlaceOnlyAvailable="
        + isPlaceOnlyAvailable
        + ", rawHandicapValue="
        + rawHandicapValue
        + ", betInRunIndex="
        + betInRunIndex
        + ", eachWayFactorNum="
        + eachWayFactorNum
        + ", eachWayFactorDen="
        + eachWayFactorDen
        + ", eachWayPlaces="
        + eachWayPlaces
        + ", isAntepost="
        + isAntepost
        + ", isResulted="
        + isResulted
        + ", isMarketBetInRun="
        + isMarketBetInRun
        + ", displayOrder="
        + displayOrder
        + ", marketStatusCode='"
        + marketStatusCode
        + '\''
        + ", isActive="
        + isActive
        + ", isDisplayed="
        + isDisplayed
        + ", flags='"
        + flags
        + '\''
        + ", siteChannels='"
        + siteChannels
        + '\''
        + ", liveServChannels='"
        + liveServChannels
        + '\''
        + ", liveServChildrenChannels='"
        + liveServChildrenChannels
        + '\''
        + ", liveServLastMsgId='"
        + liveServLastMsgId
        + '\''
        + ", priceTypeCodes='"
        + priceTypeCodes
        + '\''
        + ", ncastTypeCodes='"
        + ncastTypeCodes
        + '\''
        + ", isPoolAvailable="
        + isPoolAvailable
        + ", drilldownTagNames='"
        + drilldownTagNames
        + '\''
        + ", isWinAndPlaceAvailable="
        + isWinAndPlaceAvailable
        + ", isWPPlaceOnlyAvailable="
        + isWPPlaceOnlyAvailable
        + ", winAndPlacePlaces="
        + winAndPlacePlaces
        + ", isAvailable="
        + isAvailable
        + ", maxAccumulators="
        + maxAccumulators
        + ", isStarted="
        + isStarted
        + ", isCbAvailable="
        + isCbAvailable
        + ", isFinished="
        + isFinished
        + ", cashoutAvail='"
        + cashoutAvail
        + '\''
        + ", isRestricted="
        + isRestricted
        + ", children="
        + children
        + "} ";
  }
}
