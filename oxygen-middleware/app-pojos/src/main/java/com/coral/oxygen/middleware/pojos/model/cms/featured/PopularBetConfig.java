package com.coral.oxygen.middleware.pojos.model.cms.featured;

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

  private boolean enableBackedInTimes;
}
