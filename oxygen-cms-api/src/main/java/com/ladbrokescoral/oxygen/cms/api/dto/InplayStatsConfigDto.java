package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class InplayStatsConfigDto {
  private StatsWidgetDto statsWidgetDto;
  private StatsDisplayDto statsDisplayDto;
  private StatsSortingDto statsSortingDto;
}
