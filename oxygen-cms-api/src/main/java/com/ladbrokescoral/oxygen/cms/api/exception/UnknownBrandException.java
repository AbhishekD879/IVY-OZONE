package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.BAD_REQUEST, reason = "Unknown brand exception")
public class UnknownBrandException extends RuntimeException {

  private static final long serialVersionUID = -249294666744657034L;

  public UnknownBrandException(String brand) {
    super(brand);
  }
}
