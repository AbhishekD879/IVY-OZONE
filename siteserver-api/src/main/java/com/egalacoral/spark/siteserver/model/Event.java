package com.egalacoral.spark.siteserver.model;

import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Collectors;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class Event extends IdentityWithChildren {

  private String id;
  private String name;
  private String eventStatusCode;
  private Boolean isActive;
  private Boolean isDisplayed;
  private Integer displayOrder;
  private String siteChannels;
  private String eventSortCode;
  private String startTime;
  private String suspendAtTime;
  private String rawIsOffCode;
  private Boolean isStarted;
  private Boolean isResulted;
  private Boolean isFinished;
  private String classId;
  private String typeId;
  private String subTypeId;
  private String sportId;
  private Integer raceNumber;
  private String streamAvailableInCountries;
  private String liveServChannels;
  private String liveServChildrenChannels;
  private String liveServLastMsgId;
  private String categoryId;
  private String categoryCode;
  private String categoryName;
  private String className;
  private Integer classDisplayOrder;
  private String classSortCode;
  private String classFlagCodes;
  private String typeName;
  private Integer typeDisplayOrder;
  private String typeFlagCodes;
  private String subTypeName;
  private Integer subTypeDisplayOrder;
  private Boolean isOpenEvent;
  private Boolean isNext24HourEvent;
  private Boolean isLiveNowEvent;
  private Boolean isLiveNowOrFutureEvent;
  private String drilldownTagNames;
  private Boolean isAvailable;
  /*As part BMA-62182  new Fields at event level added from OB end to capture the same we have added
  below teamExtIds homeTeamExtIds awayTeamExtIds fields*/
  private String teamExtIds;
  private String homeTeamExtIds;
  private String awayTeamExtIds;
  private String mediaTypeCodes;
  private String venue;
  private String cashoutAvail;
  private String raceStage;
  private String responseCreationTime;
  private String effectiveGpStartTime;
  private String eventFlagCodes;

  public List<Market> getMarkets() {
    return this.getChildren().stream()
        .map(Children::getMarket)
        .filter(Objects::nonNull)
        .collect(Collectors.toList());
  }

  public List<Map<String, Object>> getEventParticipants() {
    return getConcreteChildren(Children::getEventParticipant);
  }

  public List<Map<String, Object>> getEventPeriods() {
    return getConcreteChildren(Children::getEventPeriod);
  }
}
