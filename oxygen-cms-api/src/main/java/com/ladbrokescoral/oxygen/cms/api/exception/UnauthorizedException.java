package com.ladbrokescoral.oxygen.cms.api.exception;

public class UnauthorizedException extends RuntimeException {

  private static final long serialVersionUID = 1L;

  public UnauthorizedException(String errorMessage) {
    super(errorMessage);
  }
}
