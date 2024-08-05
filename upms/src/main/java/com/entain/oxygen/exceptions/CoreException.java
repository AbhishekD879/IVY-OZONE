package com.entain.oxygen.exceptions;

public class CoreException extends Exception {

  private final String message;

  public CoreException(String message) {
    super(message);
    this.message = message;
  }

  @Override
  public String getMessage() {
    return this.message;
  }
}
