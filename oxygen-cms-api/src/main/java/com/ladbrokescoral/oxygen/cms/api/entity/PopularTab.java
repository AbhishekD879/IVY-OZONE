package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class PopularTab extends BetSlipBar {
  private String href;
  private Boolean enabled;
  private String popularTabName;
  private String headerDisplayName;
  private String startsInText;
  private String backedInLastText;
  private String showMoreText;
  private String showLessText;
  private String backedUpTimesText;
  private boolean enableBackedUpTimes;
  private boolean enableArrowIcon;
  private String informationTextDesc;
  private Integer numbOfDefaultPopularBets;
  private Integer numbOfShowMorePopularBets;
  private String priceRange;

  private String noPopularBetsMsg;
  private String lastUpdatedTime;

  private List<TimeFilters> backedInLastFilter = new ArrayList<>();
  private List<TimeFilters> eventStartsFilter = new ArrayList<>();
}
