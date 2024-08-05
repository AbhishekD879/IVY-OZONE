package com.ladbrokescoral.oxygen.cms.api.exception;

public class InputValueIncorrectException extends RuntimeException {
  private final String fieldName;
  private final String value;

  public InputValueIncorrectException(String fieldName, String value) {
    super();
    this.fieldName = fieldName;
    this.value = value;
  }

  public String getFieldName() {
    return fieldName;
  }

  public String getValue() {
    return value;
  }
}
