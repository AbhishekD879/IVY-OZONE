package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.CONFLICT, reason = "Popular Acca Widget  already exists ")
public class PopularAccaWidgetCreateException extends RuntimeException {
  public PopularAccaWidgetCreateException() {
    super();
  }
}
