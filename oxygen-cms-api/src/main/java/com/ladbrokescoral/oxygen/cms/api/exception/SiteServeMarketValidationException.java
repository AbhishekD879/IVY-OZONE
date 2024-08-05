package com.ladbrokescoral.oxygen.cms.api.exception;

public class SiteServeMarketValidationException extends RuntimeException {

  private final String message;

  public SiteServeMarketValidationException(String message) {
    super(message);
    this.message = message;
  }

  @Override
  public String getMessage() {
    return message;
  }
}
