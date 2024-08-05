package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import lombok.Data;

@Data
public class TimeFiltersDto {
  private Boolean isEnabled;
  private String displayName;
  private Boolean isTimeInHours;
  private Boolean isDefault;
  private Float time;
}
