package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.NOT_FOUND, reason = "Element not found")
public class NotFoundException extends RuntimeException {
  public NotFoundException() {
    super();
  }

  public NotFoundException(String message) {
    super(message);
  }
}
