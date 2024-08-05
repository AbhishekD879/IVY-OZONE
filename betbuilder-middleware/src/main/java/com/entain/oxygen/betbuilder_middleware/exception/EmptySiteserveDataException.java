package com.entain.oxygen.betbuilder_middleware.exception;

import lombok.Getter;

@Getter
public class EmptySiteserveDataException extends RuntimeException {
  private final String errorMessage;

  public EmptySiteserveDataException(String errorMessage) {
    this.errorMessage = errorMessage;
  }
}
