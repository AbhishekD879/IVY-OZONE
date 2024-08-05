package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SiteServeKnockoutEventDto {
  private Integer id;
  private String homeTeam;
  private String awayTeam;
  private String eventName;
  private String startTime;
}
