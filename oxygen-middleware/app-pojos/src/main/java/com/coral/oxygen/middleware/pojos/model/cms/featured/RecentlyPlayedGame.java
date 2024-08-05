package com.coral.oxygen.middleware.pojos.model.cms.featured;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class RecentlyPlayedGame extends SportPageModuleDataItem {
  private String id;
  private Integer sportId;
  private RpgConfig rpgConfig;
}
