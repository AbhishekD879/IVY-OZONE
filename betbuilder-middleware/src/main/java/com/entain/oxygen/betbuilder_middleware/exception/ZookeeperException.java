package com.entain.oxygen.betbuilder_middleware.exception;

import lombok.Getter;

@Getter
public class ZookeeperException extends RuntimeException {
  private final String errorMessage;

  public ZookeeperException(String errorMessage) {
    this.errorMessage = errorMessage;
  }
}
