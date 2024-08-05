package com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2;

/** Created by azayats on 23.11.17. */
public class RequestValidationException extends Exception {

  public RequestValidationException() {}

  public RequestValidationException(String message) {
    super(message);
  }

  public RequestValidationException(String message, Throwable cause) {
    super(message, cause);
  }

  public RequestValidationException(Throwable cause) {
    super(cause);
  }
}
