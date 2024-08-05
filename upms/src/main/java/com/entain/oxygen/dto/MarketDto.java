package com.entain.oxygen.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@SuppressWarnings("java:S1820")
public class MarketDto {
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
  private List<ChildrenDto> children;
}
