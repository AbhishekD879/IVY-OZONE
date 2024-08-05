package com.entain.oxygen.promosandbox.enums;

public enum KafkaAction {
  CREATE("Create"),
  UPDATE("Update"),
  DELETE("Delete"),
  PROMO_DATE_CHANGE("dateChange");

  private final String value;

  KafkaAction(String value) {
    this.value = value;
  }

  public String getValue() {
    return this.value;
  }
}
