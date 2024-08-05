package com.gvc.oxygen.betreceipts.entity;

import com.egalacoral.spark.siteserver.model.Market;
import com.gvc.oxygen.betreceipts.dto.HorseDTO;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class NextRace {

  private String id;
  private String name;
  private String eventStatusCode;
  private Boolean isActive; // primitive for boolean active
  private Boolean isDisplayed;
  private Integer displayOrder;
  private String siteChannels;
  private String eventSortCode;
  private String startTime;
  private String suspendAtTime;
  private String rawIsOffCode;
  private Boolean isStarted; // is/ started
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
  private List<Market> markets;

  private String diomed;
  private String courseName;
  private String goingCode;
  private String going;
  private String obStartTime;
  private Integer rpCourseId;
  private String courseGraphicsLadbrokes;
  private List<HorseDTO> horses = new ArrayList<>();
  private String courseGraphicsCoral;
  private String raceName;
  private Integer yards;
  private String distance;
  private Integer raceNo;
  private String verdict;
  private String time;
  private Integer rpRaceId;
  private Boolean isAllWeather;
  private Boolean isHandicap;
  private String flatOrJump;
  private String raceType;
  private String tv;
  private Integer raceClass;
  private String ageLimitation;
  private Integer runnerCount;
  private Integer trackFences;

  private Integer rpTrackId;
  private String fileType;
}
