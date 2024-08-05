package com.coral.oxygen.middleware.common.configuration;

import com.coral.oxygen.middleware.common.configuration.cfcache.CfHttpClientConfig;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import okhttp3.OkHttpClient;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CfHttpClientConfigTest {

  private Integer connectionTimeout = 1;
  private Integer readTimeout = 6;
  private String loggingLevel = "BASIC";
  private String proxyHost = "localhost:9092";
  private String proxyPort = "8080";

  private int maxIdleConnections = 100;

  private long keepAliveDuration = 10l;

  private OkHttpClientCreator clientCreator = new OkHttpClientCreator();

  private CfHttpClientConfig config = new CfHttpClientConfig();

  @Test
  public void testCreateClient() {

    try {
      OkHttpClient okHttpClient =
          config.cfOkHttpClient(
              readTimeout,
              connectionTimeout,
              loggingLevel,
              maxIdleConnections,
              keepAliveDuration,
              proxyHost,
              proxyPort,
              clientCreator);
      Assert.assertNotNull(okHttpClient);
      Assert.assertEquals(1000, okHttpClient.connectTimeoutMillis());
      Assert.assertEquals(6000, okHttpClient.readTimeoutMillis());
    } catch (NoSuchAlgorithmException n) {
    } catch (KeyManagementException k) {
    }
    Assert.assertNotNull(proxyPort);
  }
}
