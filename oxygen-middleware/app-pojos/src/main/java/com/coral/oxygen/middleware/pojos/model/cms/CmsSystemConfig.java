package com.coral.oxygen.middleware.pojos.model.cms;

import com.google.gson.annotations.SerializedName;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import lombok.Data;
import lombok.Getter;

/** Created by LLegkyy on 7/26/17. */
public class CmsSystemConfig {
  @SerializedName("FeaturedCategoryIdEventDisplayHours")
  Map<String, Integer> featuredCategoryIdEventDisplayHours = new HashMap<>();

  @SerializedName("BipScoreEvents")
  Map<String, Boolean> bipScoreEvents = new HashMap<>();

  @SerializedName("YourCallIconsAndTabs")
  private YourCallIconsAndTabs yourCallIconsAndTabs;

  @Getter
  @SerializedName("RacingDataHub")
  private RacingDataHub racingDataHubConfig;

  @Getter
  @SerializedName("UseFSCCached")
  private UseFSCCached useFSCCached;

  @SerializedName("NextRaces")
  private Map<String, Object> nextRaces;

  @SerializedName("GreyhoundNextRaces")
  private Map<String, Object> greyhoundNextRaces;

  public void setNextRaces(Map<String, Object> nextRaces) {
    this.nextRaces = nextRaces;
  }

  public Map<String, Object> getNextRaces() {
    return nextRaces;
  }

  public void setGreyhoundNextRaces(Map<String, Object> greyhoundNextRaces) {
    this.greyhoundNextRaces = greyhoundNextRaces;
  }

  public Map<String, Object> getGreyhoundNextRaces() {
    return greyhoundNextRaces;
  }

  public Map<String, Boolean> getBipScoreEvents() {
    return bipScoreEvents;
  }

  public void setBipScoreEvents(Map<String, Boolean> bipScoreEvents) {
    this.bipScoreEvents = bipScoreEvents;
  }

  public Map<String, Integer> getCategoryIdEventsTimeoutMap() {
    return featuredCategoryIdEventDisplayHours;
  }

  public void setFeaturedCategoryIdEventDisplayHours(
      Map<String, Integer> featuredCategoryIdEventDisplayHours) {
    this.featuredCategoryIdEventDisplayHours = featuredCategoryIdEventDisplayHours;
  }

  public YourCallIconsAndTabs getYourCallIconsAndTabs() {
    return yourCallIconsAndTabs;
  }

  public void setYourCallIconsAndTabs(YourCallIconsAndTabs yourCallIconsAndTabs) {
    this.yourCallIconsAndTabs = yourCallIconsAndTabs;
  }

  public boolean hasRacingDataHub() {
    return Optional.ofNullable(racingDataHubConfig)
        .map(RacingDataHub::getIsEnabledForHorseRacing)
        .orElse(Boolean.TRUE);
  }

  public static class YourCallIconsAndTabs {
    private Boolean enableIcon;

    public Boolean isEnableIcon() {
      return enableIcon;
    }

    public void setEnableIcon(Boolean enableIcon) {
      this.enableIcon = enableIcon;
    }
  }

  @Data
  public static class RacingDataHub {
    private Boolean isEnabledForHorseRacing;
  }

  @Data
  public static class UseFSCCached {
    private Boolean enabled;
  }

  public boolean isUseFSCCachedEnabled() {
    return Optional.ofNullable(useFSCCached).map(UseFSCCached::getEnabled).orElse(Boolean.TRUE);
  }
}
