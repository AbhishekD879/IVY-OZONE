package com.ladbrokescoral.oxygen.trendingbets.dto;

public enum PopularAccaType {
  SELECTION("SELECTION"),
  EVENT("EVENT"),
  TYPEID("TYPEID"),
  ALL("ALL");

  private final String value;

  PopularAccaType(String value) {
    this.value = value;
  }

  public String getValue() {
    return value;
  }
}
