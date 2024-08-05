package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.BAD_REQUEST, reason = "PreferenceCentre is already present")
public class PreferenceCentreCreateException extends RuntimeException {
  public PreferenceCentreCreateException(String errorMessage) {
    super();
  }
}