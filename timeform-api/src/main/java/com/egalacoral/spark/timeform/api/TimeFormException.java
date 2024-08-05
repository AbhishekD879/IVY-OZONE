package com.egalacoral.spark.timeform.api;

import java.io.IOException;

import okhttp3.ResponseBody;
import retrofit2.Response;

public class TimeFormException extends RuntimeException {

  private static String getBodyString(ResponseBody body) {
    try {
      return body.string();
    } catch (IOException e) {
      return "UNKNOWN";
    }
  }

  private Integer httpCode;

  private Response<?> response;

  public TimeFormException() {}

  public TimeFormException(String message) {
    super(message);
  }

  public TimeFormException(Response<?> response) {
    super(getBodyString(response.errorBody()));
    this.httpCode = response.code();
    this.response = response;
  }

  public TimeFormException(String message, Throwable cause) {
    super(message, cause);
  }

  public TimeFormException(Throwable cause) {
    super(cause);
  }

  public Integer getHttpCode() {
    return httpCode;
  }

  public Response<?> getResponse() {
    return response;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("TimeFormException{");
    sb.append(super.toString()).append(", ");
    sb.append("httpCode=").append(httpCode);
    sb.append(", response=").append(response);
    sb.append('}');
    return sb.toString();
  }
}
