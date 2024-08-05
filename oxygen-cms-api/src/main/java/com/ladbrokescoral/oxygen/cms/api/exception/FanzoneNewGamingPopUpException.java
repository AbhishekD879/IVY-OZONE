package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.BAD_REQUEST, reason = "Fanzone New gaming pop up already exists")
public class FanzoneNewGamingPopUpException extends RuntimeException {

  public FanzoneNewGamingPopUpException(String error) {
    super();
  }
}
