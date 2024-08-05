package com.coral.oxygen.middleware.ms.liveserv.exceptions;

/** Created by azayats on 17.05.17. */
public class ErrorResponseException extends ServiceException {

  private final int httpCode;

  private final String responseText;

  public ErrorResponseException(int httpCode, String responseText) {
    super("Error response. Code: " + httpCode + ", Body: " + responseText);
    this.httpCode = httpCode;
    this.responseText = responseText;
  }

  public int getHttpCode() {
    return httpCode;
  }

  public String getResponseText() {
    return responseText;
  }
}
