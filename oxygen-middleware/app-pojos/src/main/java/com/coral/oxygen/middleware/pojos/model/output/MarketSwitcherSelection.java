package com.coral.oxygen.middleware.pojos.model.output;

import lombok.Data;

@Data
public class MarketSwitcherSelection {
  private String marketTemplateName;
  private String templateType;
  private String marketName;
  private double handicapValue;
  private int sortOrder;
  private boolean disabled;
}
