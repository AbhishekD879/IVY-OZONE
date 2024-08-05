package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response;

import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/** Created by azayats on 24.10.17. */
@Data
@NoArgsConstructor
@AllArgsConstructor
public final class OutputMarket {
  private String id;
  private String name;
  private List<OutputOutcome> outcomes;
  private String marketStatusCode;
  private Boolean isSpAvailable = false;
  private Boolean isLpAvailable = false;
  private Boolean isGpAvailable = false;
  private Boolean isEachWayAvailable = false;
  private Integer eachWayFactorNum;
  private Integer eachWayFactorDen;
  private Boolean isMarketBetInRun = false;
  private String drilldownTagNames;
  private String isCashoutAvailable;
  private String flags;
}
