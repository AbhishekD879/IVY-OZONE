package com.coral.oxygen.middleware.ms.liveserv.client;

import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import javax.net.ssl.X509TrustManager;

class DummyTrustManager implements X509TrustManager {

  @Override
  public X509Certificate[] getAcceptedIssuers() {
    return new X509Certificate[0];
  }

  @Override
  public void checkServerTrusted(final X509Certificate[] chain, final String authType)
      throws CertificateException {
    if (chain == null || chain.length == 0)
      throw new CertificateException("No X509TrustManager implementation available");
  }

  @Override
  public void checkClientTrusted(final X509Certificate[] chain, final String authType)
      throws CertificateException {
    if (chain == null || chain.length == 0)
      throw new CertificateException("No X509TrustManager implementation available");
  }
}
