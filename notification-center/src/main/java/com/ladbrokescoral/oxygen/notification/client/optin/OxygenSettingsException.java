package com.ladbrokescoral.oxygen.notification.client.optin;

import com.newrelic.api.agent.NewRelic;
import java.io.IOException;
import okhttp3.ResponseBody;
import org.apache.commons.lang3.StringUtils;
import retrofit2.Response;

public class OxygenSettingsException extends RuntimeException {
  private Integer httpCode;
  private String requestUrl;
  private Response<?> response;

  private static String getBodyString(ResponseBody body) {
    try {
      String strBody = body.string();
      return StringUtils.isBlank(strBody) ? "EMPTY_BODY" : strBody;
    } catch (IOException var2) {
      NewRelic.noticeError(var2);
      return "UNKNOWN";
    }
  }

  public OxygenSettingsException() {}

  public OxygenSettingsException(String message) {
    super(message);
  }

  public OxygenSettingsException(String requestUrl, Response<?> response) {
    super(getBodyString(response.errorBody()));
    this.httpCode = response.code();
    this.requestUrl = requestUrl;
    this.response = response;
  }

  public OxygenSettingsException(String message, Throwable cause) {
    super(message, cause);
  }

  public OxygenSettingsException(Throwable cause) {
    super(cause);
  }

  public Response<?> getResponse() {
    return this.response;
  }

  public String toString() {
    StringBuilder sb = new StringBuilder("SiteServerException{");
    sb.append(super.toString()).append("; ");
    sb.append("httpCode=").append(this.httpCode).append("; ");
    sb.append("requestUrl=").append(this.requestUrl);
    sb.append('}');
    return sb.toString();
  }
}
