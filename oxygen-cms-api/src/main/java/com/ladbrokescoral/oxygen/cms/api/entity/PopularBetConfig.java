package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;

@Data
public class PopularBetConfig {

  private String displayName;

  private String redirectionUrl;

  private String mostBackedIn;

  private String eventStartsIn;

  private String priceRange;

  private String backedInTimes;

  private int maxSelections;

  private Integer sportId = 0;

  private boolean enableBackedInTimes;
}
