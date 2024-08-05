package com.ladbrokescoral.oxygen.cms.api.entity;

public enum MarketType {
  PB("Price Boost"),
  SPB("Super Price Boost"),
  OB("Odds Booster"),
  BMOB("Big Match Odds Booster");

  private final String description;

  MarketType(String description) {
    this.description = description;
  }

  public String getDescription() {
    return this.description;
  }
}
