package com.oxygen.publisher.model;

import java.util.List;
import lombok.Data;

/**
 * Represents the Market model. Copied from Middleware Service.
 *
 * @author tvuyiv
 */
@Data
public class OutputMarket implements IdentityAggregator {

  private String id;
  private String name;
  private Boolean isLpAvailable;
  private Boolean isSpAvailable;
  private Boolean isEachWayAvailable;
  private Boolean isGpAvailable;
  private Integer eachWayFactorNum;
  private Integer eachWayFactorDen;
  private Integer eachWayPlaces;
  private String liveServChannels;
  private String priceTypeCodes;
  private String ncastTypeCodes;
  private String cashoutAvail;
  private String handicapType;
  private String viewType;
  private String marketMeaningMajorCode;
  private String marketMeaningMinorCode;
  private String terms;
  private Boolean isMarketBetInRun;
  private Double rawHandicapValue;
  private String dispSortName;
  private String marketStatusCode;
  private Long templateMarketId;
  private String templateMarketName;
  private Integer nextScore;
  private String drilldownTagNames;
  private List<OutputOutcome> outcomes;
  private Integer displayOrder;
  private String flags;

  private String bwinId;

  private Boolean bybAvailableMarket;

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    OutputMarket that = (OutputMarket) o;
    return id.equals(that.id);
  }

  @Override
  public int hashCode() {
    int result = super.hashCode();
    result = 31 * result + id.hashCode();
    return result;
  }
}
