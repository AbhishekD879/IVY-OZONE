package com.entain.oxygen.betbuilder_middleware.exception;

public class PGConnectivityException extends RuntimeException {

  static final String ERROR_MSG = "Pricing gateway connection issue";

  public PGConnectivityException(String errorMsg) {
    super(errorMsg);
  }
}
