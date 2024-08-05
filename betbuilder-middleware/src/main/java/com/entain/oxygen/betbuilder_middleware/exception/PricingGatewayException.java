package com.entain.oxygen.betbuilder_middleware.exception;

public class PricingGatewayException extends RuntimeException {

  static final String ERROR_MSG = "Pricing gateway Exception";

  public PricingGatewayException(String errorMsg) {
    super(errorMsg);
  }
}
