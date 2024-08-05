package com.egalacoral.spark.siteserver.api;

import java.io.IOException;
import okhttp3.ResponseBody;
import retrofit2.Response;

/** Created by oleg.perushko@symphony-solutions.eu on 8/8/16 */
public class SiteServerException extends RuntimeException {

  private static String getBodyString(ResponseBody body) {
    try {
      return body.string();
    } catch (IOException e) {
      return "UNKNOWN";
    }
  }

  private Integer httpCode;

  private Response<?> response;

  public SiteServerException() {}

  public SiteServerException(String message) {
    super(message);
  }

  public SiteServerException(Response<?> response) {
    super(getBodyString(response.errorBody()));
    this.httpCode = response.code();
    this.response = response;
  }

  public SiteServerException(String message, Throwable cause) {
    super(message, cause);
  }

  public SiteServerException(Throwable cause) {
    super(cause);
  }

  public Response<?> getResponse() {
    return response;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("SiteServerException{");
    sb.append(super.toString()).append(", ");
    sb.append("httpCode=").append(httpCode);
    sb.append(", response=").append(response);
    sb.append('}');
    return sb.toString();
  }
}
