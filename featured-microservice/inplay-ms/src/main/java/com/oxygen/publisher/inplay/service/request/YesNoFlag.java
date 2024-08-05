package com.oxygen.publisher.inplay.service.request;

import lombok.Getter;

public enum YesNoFlag {
  YES("Yes"),
  NO("No");

  @Getter private final String value;

  YesNoFlag(String value) {
    this.value = value;
  }
}
