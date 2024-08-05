package com.entain.oxygen.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@SuppressWarnings("java:S1820")
public class EventDto {

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
  private List<ChildrenDto> children;
}
