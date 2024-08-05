package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.BAD_REQUEST, reason = "OddsBoostMessage is already present")
public class OddsBoostMessageCreateException extends RuntimeException {
  public OddsBoostMessageCreateException(String errorMessage) {
    super();
  }
}
