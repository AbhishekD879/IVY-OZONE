package com.coral.oxygen.middleware.ms.quickbet.connector;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.ErrorMessage;

public final class ErrorMessageFactory {
  private ErrorMessageFactory() {}

  // TODO: normalize codes
  private static final int UNAUTHORIZED_CONNECTION = 1;
  private static final int SESSION_NOT_FOUND = 2;
  private static final int INTERNAL_ERROR = 5;

  public static ErrorMessage unauthorizedConnection() {
    return new ErrorMessage(UNAUTHORIZED_CONNECTION, "Unauthorized connection");
  }

  public static ErrorMessage sessionNotFound() {
    return new ErrorMessage(SESSION_NOT_FOUND, "Session not found");
  }

  public static ErrorMessage internalError(String message) {
    return new ErrorMessage(INTERNAL_ERROR, message);
  }
}
