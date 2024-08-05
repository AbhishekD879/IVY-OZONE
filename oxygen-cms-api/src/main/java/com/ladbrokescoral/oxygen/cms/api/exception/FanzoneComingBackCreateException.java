package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.BAD_REQUEST, reason = "Fanzone coming back already exists")
public class FanzoneComingBackCreateException extends RuntimeException {
  public FanzoneComingBackCreateException(String errorMessage) {
    super();
  }
}
