package com.coral.oxygen.middleware.featured.consumer.sportpage;

public class SportsModuleProcessException extends Exception {

  public SportsModuleProcessException() {}

  public SportsModuleProcessException(String message) {
    super(message);
  }

  public SportsModuleProcessException(String message, Throwable cause) {
    super(message, cause);
  }

  public SportsModuleProcessException(Throwable cause) {
    super(cause);
  }

  public SportsModuleProcessException(
      String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace) {
    super(message, cause, enableSuppression, writableStackTrace);
  }
}
