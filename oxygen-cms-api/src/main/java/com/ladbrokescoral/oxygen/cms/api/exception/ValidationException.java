package com.ladbrokescoral.oxygen.cms.api.exception;

public class ValidationException extends RuntimeException {

  private static final String VALIDATION_MESSAGE = "Validation failed with reason: %s";

  private final String message;

  public ValidationException(String message) {
    super(message);
    this.message = String.format(VALIDATION_MESSAGE, message);
  }

  @Override
  public String getMessage() {
    return message;
  }
}
