package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;

@Data
public class InplayStatsConfig {

  private boolean showStatsWidget;

  private String note;

  private boolean showStatsDisplay;

  private boolean showStatsSorting;

  private Integer reorderDisplayIn;
}
