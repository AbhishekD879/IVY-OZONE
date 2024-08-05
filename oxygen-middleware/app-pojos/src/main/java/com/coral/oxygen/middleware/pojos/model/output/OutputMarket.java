package com.coral.oxygen.middleware.pojos.model.output;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.IdHolder;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.io.Serializable;
import java.util.Collections;
import java.util.List;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode
public class OutputMarket implements IdHolder, Serializable {

  private String id;
  private String name;
  private Boolean isLpAvailable;
  private Boolean isSpAvailable;
  protected Boolean isGpAvailable;
  private Boolean isEachWayAvailable;
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
  protected Integer displayOrder;
  private String flags;

  public String getDrilldownTagNames() {
    return drilldownTagNames;
  }

  public void setDrilldownTagNames(String drilldownTagNames) {
    this.drilldownTagNames = drilldownTagNames;
  }

  private List<OutputOutcome> outcomes;

  private String bwinId;

  private Boolean bybAvailableMarket;

  public String getBwinId() {
    return bwinId;
  }

  public void setBwinId(String bwinId) {
    this.bwinId = bwinId;
  }

  public Boolean getBybAvailableMarket() {
    return bybAvailableMarket;
  }

  public void setBybAvailableMarket(Boolean bybAvailableMarket) {
    this.bybAvailableMarket = bybAvailableMarket;
  }

  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  @ChangeDetect
  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  @JsonProperty(value = "isSpAvailable")
  @ChangeDetect
  public Boolean getSpAvailable() {
    return isSpAvailable;
  }

  public void setSpAvailable(Boolean spAvailable) {
    isSpAvailable = spAvailable;
  }

  public void setGpAvailable(Boolean gpAvailable) {
    isGpAvailable = gpAvailable;
  }

  @JsonProperty(value = "isGpAvailable")
  @ChangeDetect
  public Boolean getGpAvailable() {
    return isGpAvailable;
  }

  @JsonProperty(value = "isEachWayAvailable")
  @ChangeDetect
  public Boolean getEachWayAvailable() {
    return isEachWayAvailable;
  }

  public void setEachWayAvailable(Boolean eachWayAvailable) {
    isEachWayAvailable = eachWayAvailable;
  }

  @ChangeDetect
  public Integer getEachWayFactorNum() {
    return eachWayFactorNum;
  }

  public void setEachWayFactorNum(Integer eachWayFactorNum) {
    this.eachWayFactorNum = eachWayFactorNum;
  }

  @ChangeDetect
  public Integer getEachWayFactorDen() {
    return eachWayFactorDen;
  }

  public void setEachWayFactorDen(Integer eachWayFactorDen) {
    this.eachWayFactorDen = eachWayFactorDen;
  }

  @ChangeDetect
  public Integer getEachWayPlaces() {
    return eachWayPlaces;
  }

  public void setEachWayPlaces(Integer eachWayPlaces) {
    this.eachWayPlaces = eachWayPlaces;
  }

  @ChangeDetect
  public String getLiveServChannels() {
    return liveServChannels;
  }

  public void setLiveServChannels(String liveServChannels) {
    this.liveServChannels = liveServChannels;
  }

  @ChangeDetect
  public String getPriceTypeCodes() {
    return priceTypeCodes;
  }

  public void setPriceTypeCodes(String priceTypeCodes) {
    this.priceTypeCodes = priceTypeCodes;
  }

  @ChangeDetect
  public String getNcastTypeCodes() {
    return ncastTypeCodes;
  }

  public void setNcastTypeCodes(String ncastTypeCodes) {
    this.ncastTypeCodes = ncastTypeCodes;
  }

  @ChangeDetect
  public String getCashoutAvail() {
    return cashoutAvail;
  }

  public void setCashoutAvail(String cashoutAvail) {
    this.cashoutAvail = cashoutAvail;
  }

  @ChangeDetect
  public String getTerms() {
    return terms;
  }

  public void setTerms(String terms) {
    this.terms = terms;
  }

  @JsonProperty(value = "isLpAvailable")
  @ChangeDetect
  public Boolean getLpAvailable() {
    return isLpAvailable;
  }

  public void setLpAvailable(Boolean lpAvailable) {
    isLpAvailable = lpAvailable;
  }

  @ChangeDetect
  public String getHandicapType() {
    return handicapType;
  }

  public void setHandicapType(String handicapType) {
    this.handicapType = handicapType;
  }

  @ChangeDetect
  public String getViewType() {
    return viewType;
  }

  public void setViewType(String viewType) {
    this.viewType = viewType;
  }

  @ChangeDetect(compareCollection = true)
  public List<OutputOutcome> getOutcomes() {
    return outcomes == null ? Collections.emptyList() : outcomes;
  }

  public void setOutcomes(List<OutputOutcome> outcomes) {
    this.outcomes = outcomes;
  }

  @Override
  public String idForChangeDetection() {
    return String.valueOf(id);
  }

  public String getMarketMeaningMajorCode() {
    return marketMeaningMajorCode;
  }

  public void setMarketMeaningMajorCode(String marketMeaningMajorCode) {
    this.marketMeaningMajorCode = marketMeaningMajorCode;
  }

  public String getMarketMeaningMinorCode() {
    return marketMeaningMinorCode;
  }

  public void setMarketMeaningMinorCode(String marketMeaningMinorCode) {
    this.marketMeaningMinorCode = marketMeaningMinorCode;
  }

  @JsonProperty(value = "isMarketBetInRun")
  @ChangeDetect
  public Boolean getMarketBetInRun() {
    return isMarketBetInRun;
  }

  public void setMarketBetInRun(Boolean marketBetInRun) {
    isMarketBetInRun = marketBetInRun;
  }

  @ChangeDetect
  public Double getRawHandicapValue() {
    return rawHandicapValue;
  }

  public void setRawHandicapValue(Double rawHandicapValue) {
    this.rawHandicapValue = rawHandicapValue;
  }

  @ChangeDetect
  public String getDispSortName() {
    return dispSortName;
  }

  public void setDispSortName(String dispSortName) {
    this.dispSortName = dispSortName;
  }

  @ChangeDetect
  public String getMarketStatusCode() {
    return marketStatusCode;
  }

  public void setMarketStatusCode(String marketStatusCode) {
    this.marketStatusCode = marketStatusCode;
  }

  @ChangeDetect
  public Long getTemplateMarketId() {
    return templateMarketId;
  }

  public void setTemplateMarketId(Long templateMarketId) {
    this.templateMarketId = templateMarketId;
  }

  @ChangeDetect
  public String getTemplateMarketName() {
    return templateMarketName;
  }

  public void setTemplateMarketName(String templateMarketName) {
    this.templateMarketName = templateMarketName;
  }

  @ChangeDetect
  public Integer getNextScore() {
    return nextScore;
  }

  public void setNextScore(Integer nextScore) {
    this.nextScore = nextScore;
  }

  public Integer getDisplayOrder() {
    return displayOrder;
  }

  public void setDisplayOrder(Integer displayOrder) {
    this.displayOrder = displayOrder;
  }

  public String getFlags() {
    return flags;
  }

  public void setFlags(String flags) {
    this.flags = flags;
  }
}
