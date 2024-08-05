package com.coral.oxygen.middleware.pojos.model.output;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.gson.annotations.SerializedName;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class RacingEventData extends BasicRacingEventData {

  @SerializedName("@type")
  @JsonProperty("@type")
  private String type = "RacingEventsModuleData";

  private String categoryId;
  private String categoryName;
  private String classId;
  private String className;
  private String typeName;
  private String cashoutAvail;
  private Integer displayOrder;
  private Integer classDisplayOrder;
  private Integer typeDisplayOrder;
  private Boolean isStarted;
  private Boolean isLiveNowEvent;
  private Boolean isFinished;
  private Boolean isResulted;
  private String rawIsOffCode;
  private String typeFlagCodes;
  private String drilldownTagNames;
  private List<String> poolTypes;
  private List<RacingEventMarket> markets;

  @ChangeDetect(minor = true)
  public Boolean getIsStarted() {
    return isStarted;
  }

  @ChangeDetect(minor = true)
  public Boolean getIsFinished() {
    return isFinished;
  }

  @ChangeDetect(minor = true)
  public Boolean getIsResulted() {
    return isResulted;
  }

  @ChangeDetect(compareList = true)
  public List<RacingEventMarket> getMarkets() {
    return markets;
  }
}
