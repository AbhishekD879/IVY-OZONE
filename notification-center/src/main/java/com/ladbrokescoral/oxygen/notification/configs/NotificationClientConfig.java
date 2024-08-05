package com.ladbrokescoral.oxygen.notification.configs;

import com.turo.pushy.apns.ApnsClient;
import com.turo.pushy.apns.ApnsClientBuilder;
import com.turo.pushy.apns.auth.ApnsSigningKey;
import java.io.IOException;
import java.io.InputStream;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.Resource;

@Slf4j
@Configuration
public class NotificationClientConfig {

  public static final String QUALIFIER_APNS_CLIENT_OXYGEN = "oxygen_apns_client";
  public static final String QUALIFIER_APNS_CLIENT_HELIUM = "helium_apns_client";

  private ProxyConfig proxyConfig;

  public NotificationClientConfig(ProxyConfig proxyConfig) {
    this.proxyConfig = proxyConfig;
  }

  @Bean
  @Qualifier(QUALIFIER_APNS_CLIENT_OXYGEN)
  public ApnsClient oxygenApnsClient(
      @Value("${oxygen.apple.signing-key.path}") Resource keyFile,
      @Value("${oxygen.apple.signing-key.team}") String teamId,
      @Value("${oxygen.apple.signing-key.id}") String keyId)
      throws NoSuchAlgorithmException, InvalidKeyException, IOException {
    ApnsClientBuilder apnsClient = new ApnsClientBuilder();
    InputStream keyStream = null;
    try {
      keyStream = keyFile.getInputStream();
      apnsClient.setSigningKey(ApnsSigningKey.loadFromInputStream(keyStream, teamId, keyId));
      apnsClient.setApnsServer(ApnsClientBuilder.PRODUCTION_APNS_HOST);
    } finally {
      if (keyStream != null) {
        safeClose(keyStream);
      }
    }

    return proxyConfig.proxy(apnsClient).build();
  }

  @Bean
  @Qualifier(QUALIFIER_APNS_CLIENT_HELIUM)
  public ApnsClient heliumApnsClient(
      @Value("${helium.apple.certificate.path}") String certificate,
      @Value("${helium.apple.certificate.password}") String password)
      throws IOException {
    InputStream certificates = null;
    ApnsClientBuilder apnsClient = new ApnsClientBuilder();
    try {
      certificates = getClass().getClassLoader().getResourceAsStream(certificate);
      apnsClient.setClientCredentials(certificates, password);
      apnsClient.setApnsServer(ApnsClientBuilder.PRODUCTION_APNS_HOST);
    } finally {
      if (certificates != null) {
        safeClose(certificates);
      }
    }
    return proxyConfig.proxy(apnsClient).build();
  }

  public static void safeClose(InputStream fis) {
    if (fis != null) {
      try {
        fis.close();
      } catch (IOException e) {
        logger.error(e.getMessage());
      }
    }
  }
}
