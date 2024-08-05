package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.BAD_REQUEST, reason = "Duplicate Key will not be allowed..!")
public class ConfigMapKeyDuplicationException extends RuntimeException {

  private static final long serialVersionUID = 1L;

  public ConfigMapKeyDuplicationException(String errorMessage) {
    super(errorMessage);
  }
}
