package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.BAD_REQUEST, reason = "FanzoneNewSignposting already exists")
public class FanzoneNewSignpostingCreateException extends RuntimeException {

  public FanzoneNewSignpostingCreateException(String errorMessage) {
    super();
  }
}
