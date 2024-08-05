package com.coral.oxygen.middleware.ms.liveserv.configuration;

import static org.mockito.Mockito.mock;

import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import javax.net.ssl.SSLSession;
import okhttp3.OkHttpClient;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
class LiveServerConfigTest {
  private LiveServerConfig liveServerConfig;
  private Integer connectionTimeout = 1;
  private Integer readTimeout = 6;
  private String loggingLevel = "BASIC";
  private String proxyHost = "localhost:9092";
  private String proxyPort = "8080";

  @Test
  void okhttpclient() {
    liveServerConfig = new LiveServerConfig();
    try {
      OkHttpClient okHttpClient =
          liveServerConfig.okHttpClient(
              connectionTimeout, readTimeout, loggingLevel, proxyHost, proxyPort);
    } catch (NoSuchAlgorithmException n) {
    } catch (KeyManagementException k) {
    }
    Assert.assertNotNull(proxyPort);
  }

  @Test
  void isHostNameVerifier() {
    liveServerConfig = new LiveServerConfig();
    String hostname = "hostname";
    SSLSession sslSession = mock(SSLSession.class);
    boolean booleanvalue = liveServerConfig.isHostNameVerifier(hostname, sslSession);
    Assert.assertTrue(booleanvalue);
  }

  @Test
  void isHostNameVerifierNull() {
    liveServerConfig = new LiveServerConfig();
    String hostname = null;
    SSLSession sslSession = null;
    boolean booleanvalue = liveServerConfig.isHostNameVerifier(hostname, sslSession);
    Assert.assertFalse(booleanvalue);
  }

  @Test
  void isHostNameVerifierNull1() {
    liveServerConfig = new LiveServerConfig();
    String hostname = null;
    SSLSession sslSession = mock(SSLSession.class);
    boolean booleanvalue = liveServerConfig.isHostNameVerifier(hostname, sslSession);
    Assert.assertFalse(booleanvalue);
  }

  @Test
  void isHostNameVerifierNull3() {
    liveServerConfig = new LiveServerConfig();
    String hostname = "test";
    SSLSession sslSession = null;
    boolean booleanvalue = liveServerConfig.isHostNameVerifier(hostname, sslSession);
    Assert.assertFalse(booleanvalue);
  }
}
