package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class QuickLinkDto {
  private String title;
  private String body;
  private String linkType;
  private String target;
  private String raceType;
  private String validityPeriodStart;
  private String validityPeriodEnd;
  private String iconUrl;
  private String iconLargeUrl;
}
