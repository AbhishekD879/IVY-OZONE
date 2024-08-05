package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class StatsDisplayDto {
  private boolean showStatsDisplay;
  private List<InplayStatsDisplayDto> statsDisplayDtoList = new ArrayList<>();
}
