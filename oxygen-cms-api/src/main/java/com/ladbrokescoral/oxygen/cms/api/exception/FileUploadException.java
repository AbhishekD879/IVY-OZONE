package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.CONFLICT)
public class FileUploadException extends RuntimeException {

  public FileUploadException() {}

  public FileUploadException(String message) {
    super(message);
  }
}
