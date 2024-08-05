package com.ladbrokescoral.oxygen.seo.dto;

import java.util.List;
import lombok.Data;

@Data
public class InplayDataDto {
  // represents merged data from both sport categories & olympics
  private List<InplaySportCategoryDto> activeSportCategories;
}
