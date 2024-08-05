package com.egalacoral.spark.siteserver.api;

import com.newrelic.api.agent.NewRelic;
import java.io.IOException;
import java.util.Optional;
import okhttp3.ResponseBody;
import retrofit2.Response;

public class SiteServerException extends RuntimeException {

  private static final long serialVersionUID = 8162679898617791492L;

  private static String getBodyString(ResponseBody body) {
    try {
      String strBody = body.string();
      return Optional.ofNullable(strBody).orElse("EMPTY_BODY");
    } catch (IOException e) {
      NewRelic.noticeError(e);
      return "UNKNOWN";
    }
  }

  private Integer httpCode;
  private String requestUrl;

  private Response<?> response;

  public SiteServerException() {}

  public SiteServerException(String message) {
    super(message);
  }

  public SiteServerException(String requestUrl, Response<?> response) {
    super(getBodyString(response.errorBody()));
    this.httpCode = response.code();
    this.requestUrl = requestUrl;
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
    sb.append(super.toString()).append("; ");
    sb.append("httpCode=").append(httpCode).append("; ");
    sb.append("requestUrl=").append(requestUrl);
    sb.append('}');
    return sb.toString();
  }
}
