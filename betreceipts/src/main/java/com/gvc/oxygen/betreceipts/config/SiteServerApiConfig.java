package com.gvc.oxygen.betreceipts.config;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@ConfigurationProperties(prefix = "site-server")
@Data
@Configuration
public class SiteServerApiConfig {

  private String baseUrl;
  private String apiVersion;
  private int connectionTimeout;
  private int readTimeout;
  private int retriesNumber;
  private String loggingLevel;

  @Bean
  public SiteServerApi siteServerAPI() throws NoSuchAlgorithmException, KeyManagementException {
    return new SiteServerApi.Builder()
        .setUrl(baseUrl)
        .setLoggingLevel(SiteServerApi.Level.valueOf(loggingLevel))
        .setConnectionTimeout(connectionTimeout)
        .setReadTimeout(readTimeout)
        .setMaxNumberOfRetries(retriesNumber)
        .setVersion(apiVersion)
        .build();
  }
}
