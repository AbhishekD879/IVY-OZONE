package com.egalacoral.spark.siteserver.model;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public class Event extends Identity {
  protected List<Children> children;
  public String id;
  protected String name;
  protected String eventStatusCode;
  protected Boolean isActive;
  protected Boolean isDisplayed;
  protected Integer displayOrder;
  protected String siteChannels;
  protected String eventSortCode;
  protected String startTime;
  protected String suspendAtTime;
  protected String rawIsOffCode;
  protected Boolean isStarted;
  protected Boolean isResulted;
  protected Boolean isFinished;
  protected String classId;
  protected String typeId;
  protected String subTypeId;
  protected String sportId;
  protected Integer raceNumber;
  protected String streamAvailableInCountries;
  protected String liveServChannels;
  protected String liveServChildrenChannels;
  protected String liveServLastMsgId;
  protected String categoryId;
  protected String categoryCode;
  protected String categoryName;
  protected String className;
  protected Integer classDisplayOrder;
  protected String classSortCode;
  protected String classFlagCodes;
  protected String typeName;
  protected Integer typeDisplayOrder;
  protected String typeFlagCodes;
  protected String subTypeName;
  protected Integer subTypeDisplayOrder;
  protected Boolean isOpenEvent;
  protected Boolean isNext24HourEvent;
  protected Boolean isLiveNowEvent;
  protected Boolean isLiveNowOrFutureEvent;
  protected String drilldownTagNames;
  protected Boolean isAvailable;
  protected String mediaTypeCodes;
  protected String venue;
  protected String cashoutAvail;
  protected String raceStage;

  private List<Children> getChildren() {
    if (children == null) return new ArrayList<>();
    return children;
  }

  public List<Market> getMarkets() {
    return this.getChildren().stream()
        .map(s -> s.getMarket())
        .filter(Objects::nonNull)
        .collect(Collectors.toList());
  }

  public String getId() {
    return id;
  }

  public String getName() {
    return name;
  }

  public String getEventStatusCode() {
    return eventStatusCode;
  }

  public Boolean isActive() {
    return isActive;
  }

  public Boolean isDisplayed() {
    return isDisplayed;
  }

  public Integer getDisplayOrder() {
    return displayOrder;
  }

  public String getSiteChannels() {
    return siteChannels;
  }

  public String getEventSortCode() {
    return eventSortCode;
  }

  public String getStartTime() {
    return startTime;
  }

  public String getSuspendAtTime() {
    return suspendAtTime;
  }

  public String getRawIsOffCode() {
    return rawIsOffCode;
  }

  public Boolean isStarted() {
    return isStarted;
  }

  public Boolean isResulted() {
    return isResulted;
  }

  public Boolean isFinished() {
    return isFinished;
  }

  public String getClassId() {
    return classId;
  }

  public String getTypeId() {
    return typeId;
  }

  public String getSubTypeId() {
    return subTypeId;
  }

  public String getSportId() {
    return sportId;
  }

  public Integer getRaceNumber() {
    return raceNumber;
  }

  public String getStreamAvailableInCountries() {
    return streamAvailableInCountries;
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

  public String getCategoryId() {
    return categoryId;
  }

  public String getCategoryCode() {
    return categoryCode;
  }

  public String getCategoryName() {
    return categoryName;
  }

  public String getClassName() {
    return className;
  }

  public Integer getClassDisplayOrder() {
    return classDisplayOrder;
  }

  public String getClassSortCode() {
    return classSortCode;
  }

  public String getClassFlagCodes() {
    return classFlagCodes;
  }

  public String getTypeName() {
    return typeName;
  }

  public Integer getTypeDisplayOrder() {
    return typeDisplayOrder;
  }

  public String getTypeFlagCodes() {
    return typeFlagCodes;
  }

  public String getSubTypeName() {
    return subTypeName;
  }

  public Integer getSubTypeDisplayOrder() {
    return subTypeDisplayOrder;
  }

  public Boolean isOpenEvent() {
    return isOpenEvent;
  }

  public Boolean isNext24HourEvent() {
    return isNext24HourEvent;
  }

  public Boolean isLiveNowEvent() {
    return isLiveNowEvent;
  }

  public Boolean isLiveNowOrFutureEvent() {
    return isLiveNowOrFutureEvent;
  }

  public String getDrilldownTagNames() {
    return drilldownTagNames;
  }

  public Boolean isAvailable() {
    return isAvailable;
  }

  public String getMediaTypeCodes() {
    return mediaTypeCodes;
  }

  public String getVenue() {
    return venue;
  }

  public String getCashoutAvail() {
    return cashoutAvail;
  }

  public String getRaceStage() {
    return raceStage;
  }

  @Override
  public String toString() {
    return super.toString()
        + ", id='"
        + id
        + '\''
        + ", name='"
        + name
        + '\''
        + ", eventStatusCode='"
        + eventStatusCode
        + '\''
        + ", isActive="
        + isActive
        + ", isDisplayed="
        + isDisplayed
        + ", displayOrder="
        + displayOrder
        + ", siteChannels='"
        + siteChannels
        + '\''
        + ", eventSortCode='"
        + eventSortCode
        + '\''
        + ", startTime='"
        + startTime
        + '\''
        + ", suspendAtTime='"
        + suspendAtTime
        + '\''
        + ", rawIsOffCode='"
        + rawIsOffCode
        + '\''
        + ", isStarted="
        + isStarted
        + ", isResulted="
        + isResulted
        + ", isFinished="
        + isFinished
        + ", classId='"
        + classId
        + '\''
        + ", typeId='"
        + typeId
        + '\''
        + ", subTypeId='"
        + subTypeId
        + '\''
        + ", sportId='"
        + sportId
        + '\''
        + ", raceNumber="
        + raceNumber
        + ", streamAvailableInCountries='"
        + streamAvailableInCountries
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
        + ", categoryId='"
        + categoryId
        + '\''
        + ", categoryCode='"
        + categoryCode
        + '\''
        + ", categoryName='"
        + categoryName
        + '\''
        + ", className='"
        + className
        + '\''
        + ", classDisplayOrder="
        + classDisplayOrder
        + ", classSortCode='"
        + classSortCode
        + '\''
        + ", classFlagCodes='"
        + classFlagCodes
        + '\''
        + ", typeName='"
        + typeName
        + '\''
        + ", typeDisplayOrder="
        + typeDisplayOrder
        + ", typeFlagCodes='"
        + typeFlagCodes
        + '\''
        + ", subTypeName='"
        + subTypeName
        + '\''
        + ", subTypeDisplayOrder="
        + subTypeDisplayOrder
        + ", isOpenEvent="
        + isOpenEvent
        + ", isNext24HourEvent="
        + isNext24HourEvent
        + ", isLiveNowEvent="
        + isLiveNowEvent
        + ", isLiveNowOrFutureEvent="
        + isLiveNowOrFutureEvent
        + ", drilldownTagNames='"
        + drilldownTagNames
        + '\''
        + ", isAvailable="
        + isAvailable
        + ", mediaTypeCodes='"
        + mediaTypeCodes
        + '\''
        + ", venue='"
        + venue
        + '\''
        + ", cashoutAvail='"
        + cashoutAvail
        + '\''
        + ", raceStage='"
        + raceStage
        + '\''
        + ", children="
        + children
        + "} ";
  }
}
