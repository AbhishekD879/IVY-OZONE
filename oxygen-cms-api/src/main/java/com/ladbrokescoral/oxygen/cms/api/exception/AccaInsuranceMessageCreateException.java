package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.BAD_REQUEST, reason = "AccaInsuranceMessage is already present")
public class AccaInsuranceMessageCreateException extends RuntimeException {
  public AccaInsuranceMessageCreateException(String errorMessage) {
    super();
  }
}
