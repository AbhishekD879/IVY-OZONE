package com.coral.oxygen.middleware.pojos.model.output;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.IdHolder;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.io.Serializable;
import java.util.List;

@SuppressWarnings("java:S2160")
public class OutputOutcome extends OutcomeCodes implements IdHolder, Serializable {

  protected String id;
  protected String name;
  protected Integer runnerNumber;
  protected Boolean isResulted;
  protected String liveServChannels;
  protected String correctPriceType;
  protected Boolean icon;
  protected Integer correctedOutcomeMeaningMinorCode;
  protected Boolean nonRunner;
  private List<OutputPrice> prices;
  protected Integer displayOrder;

  private OutputRacingFormOutcome racingFormOutcome;
  private Boolean hasPriceStream;

  private String bwinId;

  public String getBwinId() {
    return bwinId;
  }

  public void setBwinId(String bwinId) {
    this.bwinId = bwinId;
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

  @ChangeDetect
  public Integer getRunnerNumber() {
    return runnerNumber;
  }

  public void setRunnerNumber(Integer runnerNumber) {
    this.runnerNumber = runnerNumber;
  }

  @ChangeDetect
  @JsonProperty(value = "isResulted")
  public Boolean getResulted() {
    return isResulted;
  }

  public void setResulted(Boolean resulted) {
    isResulted = resulted;
  }

  @ChangeDetect
  public String getLiveServChannels() {
    return liveServChannels;
  }

  public void setLiveServChannels(String liveServChannels) {
    this.liveServChannels = liveServChannels;
  }

  @ChangeDetect(compareCollection = true, minor = true)
  public List<OutputPrice> getPrices() {
    return prices;
  }

  public void setPrices(List<OutputPrice> prices) {
    this.prices = prices;
  }

  @ChangeDetect
  public String getCorrectPriceType() {
    return correctPriceType;
  }

  public void setCorrectPriceType(String correctPriceType) {
    this.correctPriceType = correctPriceType;
  }

  @ChangeDetect(compareNestedObject = true)
  public OutputRacingFormOutcome getRacingFormOutcome() {
    return racingFormOutcome;
  }

  public void setRacingFormOutcome(OutputRacingFormOutcome racingFormOutcome) {
    this.racingFormOutcome = racingFormOutcome;
    this.setIcon(racingFormOutcome != null);
  }

  @ChangeDetect
  public Integer getCorrectedOutcomeMeaningMinorCode() {
    return correctedOutcomeMeaningMinorCode;
  }

  public void setCorrectedOutcomeMeaningMinorCode(int correctedOutcomeMeaningMinorCode) {
    this.correctedOutcomeMeaningMinorCode = correctedOutcomeMeaningMinorCode;
  }

  public void clearCorrectedOutcomeMeaningMinorCode() {
    this.correctedOutcomeMeaningMinorCode = null;
  }

  @ChangeDetect
  public Boolean getIcon() {
    return icon;
  }

  public void setIcon(Boolean icon) {
    this.icon = icon;
  }

  @Override
  public String idForChangeDetection() {
    return String.valueOf(id);
  }

  @ChangeDetect
  public Boolean getNonRunner() {
    return nonRunner;
  }

  public void setNonRunner(Boolean nonRunner) {
    this.nonRunner = nonRunner;
  }

  @ChangeDetect(minor = true)
  public Integer getDisplayOrder() {
    return displayOrder;
  }

  public void setDisplayOrder(Integer displayOrder) {
    this.displayOrder = displayOrder;
  }

  public Boolean getHasPriceStream() {
    return hasPriceStream;
  }

  public void setHasPriceStream(Boolean hasPriceStream) {
    this.hasPriceStream = hasPriceStream;
  }
}
