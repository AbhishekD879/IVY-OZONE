package com.ladbrokescoral.oxygen.timeline.api.model.obevent;

import java.util.Collections;
import java.util.List;
import lombok.Data;

@Data
public class ObEvent {
  private String id;
  private String name;
  private String eventStatusCode;
  private Boolean isActive;
  private Boolean isDisplayed;
  private Integer displayOrder;

  private List<ObMarket> markets = Collections.emptyList();

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
  private String mediaTypeCodes;
  private String venue;
  private String cashoutAvail;
  private String raceStage;
  private String responseCreationTime;
  private String eventFlagCodes;

  public void applyEventUpdate(EventStatus eventStatus) {
    this.isActive = eventStatus.getActive() != null ? eventStatus.getActive() : this.isActive;
    this.isResulted =
        eventStatus.getResulted() != null ? eventStatus.getResulted() : this.isResulted;
    this.isDisplayed =
        eventStatus.getDisplayed() != null ? eventStatus.getDisplayed() : this.isDisplayed;
    this.isStarted = eventStatus.getStarted() != null ? eventStatus.getStarted() : this.isStarted;
    this.eventStatusCode = this.isActive ? "A" : "S";
  }
}
