package com.entain.oxygen.configuration;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.entain.oxygen.exceptions.SiteServeApiInitializationException;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Configuration
@Slf4j
public class SiteServerApiConfig {

  @Value("${siteserver.base.url}")
  private String siteServerUrl;

  @Value("${siteserver.api.version}")
  private String apiVersion;

  @Value("${siteserver.connection.timeout}")
  private int connectionTimeout;

  @Value("${siteserver.read.timeout}")
  private int readTimeout;

  @Value("${siteserver.retries.number}")
  private int retriesNumber;

  @Value("${siteserver.logging.level}")
  private String loggingLevel;

  public SiteServerApi siteServerAPI() {
    try {
      return new SiteServerApi.Builder()
          .setUrl(siteServerUrl)
          .setLoggingLevel(SiteServerApi.Level.valueOf(loggingLevel))
          .setConnectionTimeout(connectionTimeout)
          .setReadTimeout(readTimeout)
          .setMaxNumberOfRetries(retriesNumber)
          .setVersion(apiVersion)
          .build();
    } catch (NoSuchAlgorithmException | KeyManagementException e) {
      log.error("Error initializing SiteServerApiProvider", e);
      throw new SiteServeApiInitializationException();
    }
  }
}
