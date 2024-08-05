package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(
    value = HttpStatus.CONFLICT,
    reason = "First bet Place Tutorial is exists with enabled")
public class FirstBetPlaceTutorialCreateException extends RuntimeException {
  public FirstBetPlaceTutorialCreateException() {
    super();
  }
}
