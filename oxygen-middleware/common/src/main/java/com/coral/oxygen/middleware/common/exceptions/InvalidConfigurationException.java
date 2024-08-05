package com.coral.oxygen.middleware.common.exceptions;

public class InvalidConfigurationException extends RuntimeException {
  public InvalidConfigurationException(String message, Throwable e) {
    super(message, e);
  }

  public InvalidConfigurationException(String message) {
    super(message);
  }
}
