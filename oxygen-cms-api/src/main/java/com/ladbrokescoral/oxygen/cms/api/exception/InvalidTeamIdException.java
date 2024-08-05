package com.ladbrokescoral.oxygen.cms.api.exception;

import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.NOT_FOUND, reason = "Invalid TeamId")
@AllArgsConstructor
public class InvalidTeamIdException extends RuntimeException {
  public InvalidTeamIdException(String message) {
    super(message);
  }
}
