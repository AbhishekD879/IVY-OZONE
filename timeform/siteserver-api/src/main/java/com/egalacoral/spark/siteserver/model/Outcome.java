package com.egalacoral.spark.siteserver.model;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public class Outcome extends Identity {
  protected List<Children> children;
  protected String id;
  protected String marketId;
  protected String name;
  protected String outcomeMeaningMajorCode;
  protected String outcomeMeaningMinorCode;
  protected String outcomeMeaningScores;
  protected Integer runnerNumber;
  protected Boolean isResulted;
  protected Integer displayOrder;
  protected String outcomeStatusCode;
  protected Boolean isActive;
  protected Boolean isDisplayed;
  protected String siteChannels;
  protected String liveServChannels;
  protected String liveServChildrenChannels;
  protected String liveServLastMsgId;
  protected String drilldownTagNames;
  protected Boolean isAvailable;
  protected Boolean isFinished;
  protected String hasRestrictedSet;
  protected Boolean isEnhancedOdds;
  protected String cashoutAvail;

  private List<Children> getChildren() {
    if (children == null) return new ArrayList<>();
    return children;
  }

  public List<Price> getPrices() {
    return this.getChildren().stream()
        .map(s -> s.getPrice())
        .filter(Objects::nonNull)
        .collect(Collectors.toList());
  }

  public String getId() {
    return id;
  }

  public String getMarketId() {
    return marketId;
  }

  public String getName() {
    return name;
  }

  public String getOutcomeMeaningMajorCode() {
    return outcomeMeaningMajorCode;
  }

  public String getOutcomeMeaningMinorCode() {
    return outcomeMeaningMinorCode;
  }

  public String getOutcomeMeaningScores() {
    return outcomeMeaningScores;
  }

  public Integer isRunnerNumber() {
    return runnerNumber;
  }

  public Boolean isResulted() {
    return isResulted;
  }

  public Integer getDisplayOrder() {
    return displayOrder;
  }

  public String getOutcomeStatusCode() {
    return outcomeStatusCode;
  }

  public Boolean isActive() {
    return isActive;
  }

  public Boolean isDisplayed() {
    return isDisplayed;
  }

  public String getSiteChannels() {
    return siteChannels;
  }

  public String getLiveServChannels() {
    return liveServChannels;
  }

  public String getLiveServChildrenChannels() {
    return liveServChildrenChannels;
  }

  public String getLiveServLastMsgId() {
    return liveServLastMsgId;
  }

  public String getDrilldownTagNames() {
    return drilldownTagNames;
  }

  public Boolean isAvailable() {
    return isAvailable;
  }

  public Boolean isFinished() {
    return isFinished;
  }

  public String getHasRestrictedSet() {
    return hasRestrictedSet;
  }

  public Boolean isEnhancedOdds() {
    return isEnhancedOdds;
  }

  public String isCashoutAvail() {
    return cashoutAvail;
  }

  @Override
  public String toString() {
    return super.toString()
        + ", id='"
        + id
        + '\''
        + ", marketId='"
        + marketId
        + '\''
        + ", name='"
        + name
        + '\''
        + ", outcomeMeaningMajorCode='"
        + outcomeMeaningMajorCode
        + '\''
        + ", outcomeMeaningMinorCode='"
        + outcomeMeaningMinorCode
        + '\''
        + ", outcomeMeaningScores='"
        + outcomeMeaningScores
        + '\''
        + ", runnerNumber="
        + runnerNumber
        + ", isResulted="
        + isResulted
        + ", displayOrder="
        + displayOrder
        + ", outcomeStatusCode='"
        + outcomeStatusCode
        + '\''
        + ", isActive="
        + isActive
        + ", isDisplayed="
        + isDisplayed
        + ", siteChannels='"
        + siteChannels
        + '\''
        + ", liveServChannels='"
        + liveServChannels
        + '\''
        + ", liveServChildrenChannels='"
        + liveServChildrenChannels
        + '\''
        + ", liveServLastMsgId='"
        + liveServLastMsgId
        + '\''
        + ", drilldownTagNames='"
        + drilldownTagNames
        + '\''
        + ", isAvailable="
        + isAvailable
        + ", isFinished="
        + isFinished
        + ", hasRestrictedSet='"
        + hasRestrictedSet
        + '\''
        + ", isEnhancedOdds="
        + isEnhancedOdds
        + ", cashoutAvail='"
        + cashoutAvail
        + '\''
        + ", children="
        + children
        + "} ";
  }
}
