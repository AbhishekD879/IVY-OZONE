package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class SiteServeCompleteMarketDto {
  private String id;
  private String name;
  private Boolean isLpAvailable;
  private Boolean isSpAvailable;
  private Boolean isGpAvailable;
  private Integer eachWayFactorNum;
  private Integer eachWayFactorDen;
  private Integer eachWayPlaces;
  private String liveServChannels;
  private String priceTypeCodes;
  private String ncastTypeCodes;
  private String cashoutAvail;
  private String marketMeaningMajorCode;
  private String marketMeaningMinorCode;
  private Boolean isMarketBetInRun;
  private Double rawHandicapValue;
  private String dispSortName;
  private String marketStatusCode;
  private Long templateMarketId;
  private String templateMarketName;
  private String drilldownTagNames;
  private Integer displayOrder;
  private String flags;
  private List<SiteServeCompleteOutcomeDto> outcomes;
}
