package com.ladbrokescoral.oxygen.cms.api.exception;

public class InternalServerException extends RuntimeException {

  public InternalServerException(String message) {
    super(message);
  }

  public InternalServerException(String message, Throwable cause) {
    super(message, cause);
  }
}
