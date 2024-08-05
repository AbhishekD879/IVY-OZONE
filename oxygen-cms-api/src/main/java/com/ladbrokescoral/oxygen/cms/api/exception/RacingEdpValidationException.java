package com.ladbrokescoral.oxygen.cms.api.exception;

import lombok.Getter;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(
    value = HttpStatus.INTERNAL_SERVER_ERROR,
    reason =
        "There May be More than two items with same name or Market with same name in repo posses duplicate fields")
@Getter
public class RacingEdpValidationException extends RuntimeException {

  private static final String RACING_VALIDATION_MESSAGE = "Validation Failed with the Reason: %s";

  private final String message;

  public RacingEdpValidationException(String message) {
    super(message);
    this.message = String.format(RACING_VALIDATION_MESSAGE, message);
  }
}
