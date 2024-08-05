package com.entain.oxygen.promosandbox.exception;

public class BppTokenRequiredException extends RuntimeException {
  private static final long serialVersionUID = 1L;

  public BppTokenRequiredException(String message) {
    super(message);
  }
}
