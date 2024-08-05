package com.entain.oxygen.util;

public enum Preference {
  FRACTIONAL("frac"),
  DECIMAL("dec"),
  AMERICAN("ame");

  private final String value;

  Preference(String value) {
    this.value = value;
  }

  public String value() {
    return this.value;
  }
}
