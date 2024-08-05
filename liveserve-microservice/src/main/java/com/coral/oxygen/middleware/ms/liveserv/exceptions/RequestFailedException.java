package com.coral.oxygen.middleware.ms.liveserv.exceptions;

/** Created by azayats on 18.05.17. */
public class RequestFailedException extends ServiceException {
  public RequestFailedException(String message) {
    super(message);
  }

  public RequestFailedException(String message, Throwable cause) {
    super(message, cause);
  }
}
