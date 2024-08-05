package com.entain.oxygen.promosandbox.enums;

public enum FileProcessStatus {
  SUCCESS("Success"),
  FAILURE("Failure");
  private final String value;

  FileProcessStatus(String value) {
    this.value = value;
  }

  public String getValue() {
    return this.value;
  }
}
