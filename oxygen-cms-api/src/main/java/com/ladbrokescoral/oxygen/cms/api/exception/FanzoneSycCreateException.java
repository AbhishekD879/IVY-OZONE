package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.BAD_REQUEST, reason = "FanzoneSyc is already present")
public class FanzoneSycCreateException extends RuntimeException {
  public FanzoneSycCreateException(String errorMessage) {
    super();
  }
}
