package com.coral.oxygen.edp.model.mapping.config;

public enum OddsCardHeaderType {
  HOME_DRAW_AWAY("homeDrawAwayType"),
  ONE_THREE("oneThreeType"),
  ONE_TWO("oneTwoType");

  private final String name;

  OddsCardHeaderType(String name) {
    this.name = name;
  }

  public static OddsCardHeaderType from(String typeName) {
    for (OddsCardHeaderType type : OddsCardHeaderType.values()) {
      if (type.name.equals(typeName)) {
        return type;
      }
    }
    throw new IllegalArgumentException(typeName);
  }

  @Override
  public String toString() {
    return this.name;
  }
}
