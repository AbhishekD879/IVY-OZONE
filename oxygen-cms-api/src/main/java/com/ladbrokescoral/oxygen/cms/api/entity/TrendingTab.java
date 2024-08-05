package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import org.springframework.data.mongodb.core.mapping.DBRef;

@Data
public class TrendingTab extends SortableEntity implements HasBrand {

  private String brand;
  private Integer sportId;
  private String trendingTabName;
  private String headerDisplayName;
  private boolean enabled;
  private String href;
  @DBRef private List<PopularTab> popularTabs = new ArrayList<>();
}
