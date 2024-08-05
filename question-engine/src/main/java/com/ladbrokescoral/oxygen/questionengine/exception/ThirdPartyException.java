package com.ladbrokescoral.oxygen.questionengine.exception;

public class ThirdPartyException extends RuntimeException {
  public ThirdPartyException(String message, Exception ex) {
    super(message, ex);
  }

  public ThirdPartyException(String message) {
    super(message);
  }
}
