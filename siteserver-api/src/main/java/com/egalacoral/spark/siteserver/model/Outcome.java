package com.egalacoral.spark.siteserver.model;

import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class Outcome extends IdentityWithChildren {

  private String id;
  private String marketId;
  private String name;
  private String outcomeMeaningMajorCode;
  private String outcomeMeaningMinorCode;
  private String outcomeMeaningScores;
  private Integer runnerNumber;
  private Boolean isResulted;
  private Integer displayOrder;
  private String outcomeStatusCode;
  private Boolean isActive;
  private Boolean isDisplayed;
  private String siteChannels;
  private String liveServChannels;
  private String liveServChildrenChannels;
  private String liveServLastMsgId;
  private String drilldownTagNames;
  private Boolean isAvailable;
  private Boolean isFinished;
  private String hasRestrictedSet;
  private Boolean isEnhancedOdds;
  private String cashoutAvail;
  private String resultCode;
  private String position;
  private boolean hasPriceStream;

  public List<Price> getPrices() {
    return getConcreteChildren(Children::getPrice);
  }
}
