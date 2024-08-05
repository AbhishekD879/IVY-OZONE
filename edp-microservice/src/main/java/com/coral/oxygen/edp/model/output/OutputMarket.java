package com.coral.oxygen.edp.model.output;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.Collections;
import java.util.List;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class OutputMarket {

  private String id;
  private String name;
  private Boolean isLpAvailable;
  private Boolean isSpAvailable;
  protected Boolean isGpAvailable;
  private Integer eachWayFactorNum; // ?
  private Integer eachWayFactorDen; // ?
  private Integer eachWayPlaces;
  private String liveServChannels;
  private String priceTypeCodes;
  private String ncastTypeCodes; // ?
  private String cashoutAvail;
  private String handicapType;
  private String viewType;
  private String marketMeaningMajorCode;
  private String marketMeaningMinorCode;
  private String terms;
  private Boolean isMarketBetInRun;
  protected Double rawHandicapValue;
  protected String dispSortName;
  private String marketStatusCode;
  private Long templateMarketId;
  private String templateMarketName;
  private Integer nextScore;
  private String drilldownTagNames;
  private Integer displayOrder;
  private Boolean isEachWayAvailable;
  private String flags;
  private List<OutputOutcome> outcomes;

  public List<OutputOutcome> getOutcomes() {
    return outcomes == null ? Collections.emptyList() : outcomes;
  }
}
