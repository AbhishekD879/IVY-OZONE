package com.ladbrokescoral.cashout.model;

public enum SSEType {
  INITIAL("initial"),
  CASHOUT_UPDATE("cashoutUpdate"),
  BET_UPDATE("betUpdate");

  private String value;

  SSEType(String value) {
    this.value = value;
  }

  public String getValue() {
    return value;
  }
}
