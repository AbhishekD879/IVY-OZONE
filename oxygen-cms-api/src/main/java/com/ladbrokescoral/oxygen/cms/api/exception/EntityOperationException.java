package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.CONFLICT, reason = "Issue with entity operaition")
public class EntityOperationException extends RuntimeException {

  public EntityOperationException(String s) {
    super(s);
  }
}
