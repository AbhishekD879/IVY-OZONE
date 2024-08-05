package com.coral.oxygen.middleware.pojos.model.cms.featured;

import lombok.Data;

@Data
public class RacingConfig {
  private String abbreviation;
  private boolean enablePoolIndicators;
  private int eventsSelectionDays;
  private int limit;
  private String excludeTypeIds;
  private int classId;
  private int timeRangeHours;
}
