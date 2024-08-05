package com.coral.oxygen.middleware.pojos.model.cms;

public enum EventLoadingType {
  SELECTION_ID("Selection"),
  TYPE_ID("Type"),
  RACE_TYPE_ID("RaceTypeId"),
  ENHANCED_MULTIPLES("Enhanced Multiples"), // [2297]
  RACING_GRID("RacingGrid"),
  MARKET_ID("Market");

  private String value;

  EventLoadingType(String value) {
    this.value = value;
  }

  public String getValue() {
    return value;
  }

  public boolean isTypeOf(String selectionType) {
    return this.getValue().equalsIgnoreCase(selectionType);
  }
}
