package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.CONFLICT, reason = "Byb Widget  already exists ")
public class BybWidgetCreateException extends RuntimeException {
  public BybWidgetCreateException() {
    super();
  }
}
