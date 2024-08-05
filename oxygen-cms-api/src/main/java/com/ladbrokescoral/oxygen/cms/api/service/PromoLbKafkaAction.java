package com.ladbrokescoral.oxygen.cms.api.service;

public enum PromoLbKafkaAction {
  CREATE("Create"),
  UPDATE("Update"),
  DELETE("Delete"),
  PROMO_DATE_CHANGE("dateChange");

  PromoLbKafkaAction(String value) {
    this.value = value;
  }

  private String value;

  public String getValue() {
    return this.value;
  }
}
