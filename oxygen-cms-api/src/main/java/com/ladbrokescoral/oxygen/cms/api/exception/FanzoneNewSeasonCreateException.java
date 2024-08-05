package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.BAD_REQUEST, reason = "Fanzone new season already exists")
public class FanzoneNewSeasonCreateException extends RuntimeException {
  public FanzoneNewSeasonCreateException(String errorMessage) {
    super();
  }
}
