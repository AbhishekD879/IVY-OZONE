package com.entain.oxygen.exceptions;

public class UserStableException extends CoreException {
  private final int errorCode;

  public UserStableException(String message, int errorCode) {
    super(message);
    this.errorCode = errorCode;
  }

  public int getErrorCode() {
    return errorCode;
  }
}
