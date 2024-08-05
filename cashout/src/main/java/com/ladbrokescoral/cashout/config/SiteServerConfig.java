package com.ladbrokescoral.cashout.config;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SiteServerConfig {

  @Value("${siteserver.api.version}")
  private String apiVersion;

  @Value("${siteserver.api.latest.version}")
  private String latestApiVersion;

  @Value("${siteserver.priceboost.enabled}")
  private boolean isPriceBoostEnabled;

  @Bean
  public SiteServerApi siteServerApi(
      @Value("${siteServer.base.url}") String siteServerUrl,
      @Value("${siteServer.connection.timeout:1}") int connectionTimeout,
      @Value("${siteServer.read.timeout:1}") int readTimeout,
      @Value("${siteServer.retries.number:1}") int retriesNumber,
      @Value("${siteServer.logging.level:BASIC}") String loggingLevel)
      throws NoSuchAlgorithmException, KeyManagementException {
    return new SiteServerApi.Builder()
        .setUrl(siteServerUrl)
        .setLoggingLevel(SiteServerApi.Level.valueOf(loggingLevel))
        .setConnectionTimeout(connectionTimeout)
        .setReadTimeout(readTimeout)
        .setMaxNumberOfRetries(retriesNumber)
        .setVersion(getapiVersion())
        .build();
  }

  private String getapiVersion() {
    if (isPriceBoostEnabled) {
      return latestApiVersion;
    }
    return apiVersion;
  }
}
