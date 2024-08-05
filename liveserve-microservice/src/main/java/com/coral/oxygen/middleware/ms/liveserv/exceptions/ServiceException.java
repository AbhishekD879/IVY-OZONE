package com.coral.oxygen.middleware.ms.liveserv.exceptions;

/** Created by azayats on 08.05.17. */
public class ServiceException extends Exception {

  public ServiceException() {}

  public ServiceException(String message) {
    super(message);
  }

  public ServiceException(String message, Throwable cause) {
    super(message, cause);
  }

  public ServiceException(Throwable cause) {
    super(cause);
  }
}
