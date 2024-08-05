package com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class MarketDto {
  private String id;
  private String eventId;
  private Long templateMarketId;
  private String templateMarketName;
  private String dispSortName;
  private String marketMeaningMajorCode;
  private String marketMeaningMinorCode;
  private String name;
  private Boolean isDisplayed;
  private Boolean isLpAvailable = false;
  private Boolean isSpAvailable = false;
  private Boolean isGpAvailable = false;
  private Boolean isEachWayAvailable = false;
  private Integer eachWayFactorNum;
  private Integer eachWayFactorDen;
  private Integer eachWayPlaces;
  private Boolean isMarketBetInRun;
  private Integer displayOrder;
  private String marketStatusCode;
  private String liveServChannels;
  private String priceTypeCodes;
  private String drilldownTagNames;
  private String cashoutAvail;
  private String flags;
  private List<OutcomeDto> outcomes = new ArrayList<>();
}
