package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.Arrays;

public enum PopularAccaType {
  SELECTION("SELECTION"),
  EVENT("EVENT"),
  TYPEID("LEAGUE"),
  ALL("ALL");

  private final String value;

  PopularAccaType(String value) {
    this.value = value;
  }

  public String getValue() {
    return value;
  }

  public static PopularAccaType getPopularAccaType(String type) {
    return Arrays.stream(values())
        .filter(accaType -> accaType.getValue().equalsIgnoreCase(type))
        .findFirst()
        .orElse(ALL);
  }
}
