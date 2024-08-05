package com.ladbrokescoral.oxygen.notification.services;

public class ConsumeEventException extends RuntimeException {

  public ConsumeEventException(String message) {
    super(message);
  }

  public ConsumeEventException(String message, Throwable cause) {
    super(message, cause);
  }
}
