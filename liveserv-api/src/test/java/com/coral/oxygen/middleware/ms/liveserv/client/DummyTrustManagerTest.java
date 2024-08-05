package com.coral.oxygen.middleware.ms.liveserv.client;

import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertThrows;

import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class DummyTrustManagerTest {

  private DummyTrustManager dummyTrustManager;

  @Mock private X509Certificate certificate;

  @Before
  public void setUp() {
    dummyTrustManager = new DummyTrustManager();
  }

  @Test
  public void testGetAcceptedIssuers() {
    X509Certificate[] ret = dummyTrustManager.getAcceptedIssuers();
    assertArrayEquals(new X509Certificate[0], ret);
  }

  @Test
  public void testCheckServerTrusted() throws CertificateException {
    dummyTrustManager.checkServerTrusted(new X509Certificate[] {certificate}, "RSA");
  }

  @Test
  public void testCheckServerTrustedEmptyCertificate() {
    assertThrows(
        "Expected dummyTrustManager.checkServerTrusted to throw, but it didn't",
        CertificateException.class,
        () -> dummyTrustManager.checkServerTrusted(new X509Certificate[] {}, "RSA"));

    assertThrows(
        "Expected dummyTrustManager.checkServerTrusted to throw, but it didn't",
        CertificateException.class,
        () -> dummyTrustManager.checkServerTrusted(null, "RSA"));
  }

  @Test
  public void testCheckClientTrustedEmptyCertificate() {
    assertThrows(
        "Expected dummyTrustManager.checkClientTrusted to throw, but it didn't",
        CertificateException.class,
        () -> dummyTrustManager.checkClientTrusted(new X509Certificate[] {}, "RSA"));

    assertThrows(
        "Expected dummyTrustManager.checkClientTrusted to throw, but it didn't",
        CertificateException.class,
        () -> dummyTrustManager.checkClientTrusted(null, "RSA"));
  }

  @Test
  public void testCheckClientTrusted() throws CertificateException {
    dummyTrustManager.checkClientTrusted(new X509Certificate[] {certificate}, "RSA");
  }
}
