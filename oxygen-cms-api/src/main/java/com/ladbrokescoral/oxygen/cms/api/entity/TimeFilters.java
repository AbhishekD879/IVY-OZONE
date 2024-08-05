package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;

@Data
public class TimeFilters {
  private Boolean isEnabled;
  private String displayName;
  private Boolean isTimeInHours;
  private Boolean isDefault;
  private Float time;
}
