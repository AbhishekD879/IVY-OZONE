package com.coral.oxygen.middleware.common.configuration;

import java.net.InetSocketAddress;
import java.net.Proxy;
import java.net.Proxy.Type;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.X509Certificate;
import java.util.concurrent.TimeUnit;
import javax.net.ssl.*;
import lombok.extern.slf4j.Slf4j;
import okhttp3.ConnectionPool;
import okhttp3.OkHttpClient;
import okhttp3.OkHttpClient.Builder;
import okhttp3.logging.HttpLoggingInterceptor;
import org.apache.logging.log4j.util.Strings;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class OkHttpClientCreator {
  public OkHttpClient createOkHttpClient(
      long connectionTimeout,
      long readTimeout,
      int maxIdleConnections,
      long keepAliveDuration,
      HttpLoggingInterceptor.Logger logger,
      String loggingLevel,
      String proxyHost,
      String proxyPort)
      throws NoSuchAlgorithmException, KeyManagementException {
    HttpLoggingInterceptor interceptor = new HttpLoggingInterceptor(logger);
    interceptor.setLevel(HttpLoggingInterceptor.Level.valueOf(loggingLevel));

    log.warn("**** Allow untrusted SSL connection ****");
    final TrustManager[] listOfTrustManagers = new TrustManager[] {new BlindTrustManager()};
    SSLContext sslContext = SSLContext.getInstance("TLSv1.2");
    sslContext.init(null, listOfTrustManagers, new java.security.SecureRandom());

    Builder clientBuilder =
        new Builder()
            .addInterceptor(interceptor)
            .connectionPool(
                new ConnectionPool(maxIdleConnections, keepAliveDuration, TimeUnit.SECONDS))
            .readTimeout(readTimeout, TimeUnit.SECONDS)
            .connectTimeout(connectionTimeout, TimeUnit.SECONDS)
            .sslSocketFactory(
                sslContext.getSocketFactory(), (X509TrustManager) listOfTrustManagers[0])
            .hostnameVerifier(OkHttpClientCreator::hostNameSessionVerifier);
    if (Strings.isNotBlank(proxyHost) && Strings.isNotBlank(proxyPort)) {
      return clientBuilder
          .proxy(
              new Proxy(Type.HTTP, new InetSocketAddress(proxyHost, Integer.parseInt(proxyPort))))
          .build();
    }
    return clientBuilder.build();
  }

  public static boolean hostNameSessionVerifier(String hostname, SSLSession sslSession) {
    return (hostname != null && sslSession != null);
  }

  static class BlindTrustManager implements X509TrustManager {
    @Override
    public X509Certificate[] getAcceptedIssuers() {
      return new X509Certificate[0];
    }

    @Override
    public void checkServerTrusted(final X509Certificate[] chain, final String authType) {
      // N/A
    }

    @Override
    public void checkClientTrusted(final X509Certificate[] chain, final String authType) {
      // N/A
    }
  }
}
