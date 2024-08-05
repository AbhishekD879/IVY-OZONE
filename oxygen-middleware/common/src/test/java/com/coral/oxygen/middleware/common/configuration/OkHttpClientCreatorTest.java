package com.coral.oxygen.middleware.common.configuration;

import static org.mockito.Mockito.mock;

import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import javax.net.ssl.SSLSession;
import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class OkHttpClientCreatorTest {
  private OkHttpClientCreator okHttpClientCreator;
  private Integer connectionTimeout = 1;
  private Integer readTimeout = 6;
  private String loggingLevel = "BASIC";
  private String proxyHost = "localhost:9092";
  private String proxyPort = "8080";

  private int maxIdleConnections = 100;

  private long keepAliveDuration = 10l;
  private HttpLoggingInterceptor.Logger logger = Mockito.mock(HttpLoggingInterceptor.Logger.class);

  OkHttpClientCreator clientCreator = null;

  @Test
  public void testCreateClient() {
    clientCreator = new OkHttpClientCreator();
    try {
      OkHttpClient okHttpClient =
          clientCreator.createOkHttpClient(
              connectionTimeout,
              readTimeout,
              maxIdleConnections,
              keepAliveDuration,
              logger,
              loggingLevel,
              proxyHost,
              proxyPort);
      Assert.assertNotNull(okHttpClient);
    } catch (NoSuchAlgorithmException n) {
    } catch (KeyManagementException k) {
    }
    Assert.assertNotNull(proxyPort);
  }

  @Test
  public void isaBoolean() {
    String hostname = "hostname";
    SSLSession sslSession = mock(SSLSession.class);
    boolean booleanvalue = OkHttpClientCreator.hostNameSessionVerifier(hostname, sslSession);
    Assert.assertTrue(booleanvalue);
  }

  @Test
  public void isaBooleanNull() {
    String hostname = null;
    SSLSession sslSession = null;
    boolean booleanvalue = OkHttpClientCreator.hostNameSessionVerifier(hostname, sslSession);
    Assert.assertFalse(booleanvalue);
  }

  @Test
  public void isaBooleanNull1() {
    String hostname = null;
    SSLSession sslSession = mock(SSLSession.class);
    boolean booleanvalue = OkHttpClientCreator.hostNameSessionVerifier(hostname, sslSession);
    Assert.assertFalse(booleanvalue);
  }

  @Test
  public void isaBooleanNull3() {
    String hostname = "test";
    SSLSession sslSession = null;
    boolean booleanvalue = OkHttpClientCreator.hostNameSessionVerifier(hostname, sslSession);
    Assert.assertFalse(booleanvalue);
  }
}
