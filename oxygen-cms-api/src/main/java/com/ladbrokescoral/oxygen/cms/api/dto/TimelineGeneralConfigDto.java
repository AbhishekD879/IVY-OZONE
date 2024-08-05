package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class TimelineGeneralConfigDto {
  private String id;

  private boolean enabled;
  private String pageUrls;

  private String liveCampaignId;
  private String liveCampaignName;
  private Instant liveCampaignDisplayFrom;
  private Instant liveCampaignDisplayTo;
}
