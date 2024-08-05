package com.entain.oxygen.util;

public enum Brand {
  BMA("bma"),
  LADBROKES("ladbrokes"),
  CONNECT("connect"),
  RETAIL("retail");

  private final String value;

  Brand(String value) {
    this.value = value;
  }

  public String value() {
    return this.value;
  }
}
