package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import java.util.Map;
import lombok.Data;

@Data
public class InplayDataDto {
  // represents merged data from both sport categories & olympics
  private List<InplaySportCategoryDto> activeSportCategories;
  private Map<Integer, InplaySportCategoryDto> sportMap;
  private List<VirtualSportDto> virtualSports;
}
