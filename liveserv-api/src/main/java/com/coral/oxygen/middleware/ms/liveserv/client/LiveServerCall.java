package com.coral.oxygen.middleware.ms.liveserv.client;

import com.coral.oxygen.middleware.ms.liveserv.exceptions.ErrorResponseException;
import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;
import com.newrelic.api.agent.Trace;
import java.io.IOException;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.time.Duration;
import java.util.Objects;
import java.util.concurrent.TimeUnit;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import okhttp3.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class LiveServerCall implements Call {

  private static final Logger LOGGER = LoggerFactory.getLogger(LiveServerCall.class);
  private static final MediaType MEDIA_TYPE_MARKDOWN =
      MediaType.parse("text/x-markdown; charset=utf-8");
  private final OkHttpClient client;
  private final String endPoint;

  public LiveServerCall(
      String endPoint,
      long connectTimeout,
      long readTimeOut,
      int maxIdleConnections,
      Duration keepAliveDuration)
      throws NoSuchAlgorithmException, KeyManagementException {

    this.endPoint = endPoint;

    LOGGER.warn("**** Allow untrusted SSL connection ****");

    final TrustManager[] listOfTrustManagers = {new DummyTrustManager()};

    SSLContext sslContext = SSLContext.getInstance("TLS");
    sslContext.init(null, listOfTrustManagers, new java.security.SecureRandom());

    client =
        new OkHttpClient.Builder()
            .connectionPool(
                new ConnectionPool(
                    maxIdleConnections, keepAliveDuration.getSeconds(), TimeUnit.SECONDS))
            .readTimeout(readTimeOut, TimeUnit.SECONDS)
            .connectTimeout(connectTimeout, TimeUnit.SECONDS)
            .retryOnConnectionFailure(false)
            .sslSocketFactory(
                sslContext.getSocketFactory(), (X509TrustManager) listOfTrustManagers[0])
            .hostnameVerifier(
                (hostname, session) -> hostname.equalsIgnoreCase(session.getPeerHost()))
            .build();
  }

  @Override
  @Trace
  public String execute(String requestBody) throws IOException, ServiceException {

    LOGGER.debug("REQUEST: {}", requestBody);
    Request request =
        new Request.Builder()
            .url(endPoint)
            .post(RequestBody.create(MEDIA_TYPE_MARKDOWN, requestBody))
            .build();
    Response response = client.newCall(request).execute();
    LOGGER.debug("RESPONSE:  {}", response);
    return getResponseBody(response);
  }

  String getResponseBody(Response response) throws IOException, ErrorResponseException {
    String responseBody = null;
    if (Objects.nonNull(response.body())) {
      responseBody = response.body().string();
    }
    if (response.isSuccessful()) {
      return responseBody;
    } else {
      int code = response.code();
      LOGGER.error("Error response from LiveServ. Code: {}, Body: {}", code, responseBody);
      throw new ErrorResponseException(code, responseBody);
    }
  }
}
