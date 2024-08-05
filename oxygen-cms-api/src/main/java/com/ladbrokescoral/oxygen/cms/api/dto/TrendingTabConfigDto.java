package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class TrendingTabConfigDto {

  private String id;
  private Double sortOrder;
  private String brand;
  private Integer sportId;
  private String trendingTabName;
  private String headerDisplayName;
  private boolean enabled;
  private String href;
  private List<PopularTabConfigDto> popularTabs;
}
