package com.entain.oxygen.betbuilder_middleware.exception;

public class BetBuilderException extends RuntimeException {

  static final String ERROR_MSG = "Error Due to unknown Exception";

  public BetBuilderException(String errorMsg) {
    super(errorMsg);
  }
}
