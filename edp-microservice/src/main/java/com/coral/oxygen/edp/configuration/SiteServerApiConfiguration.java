package com.coral.oxygen.edp.configuration;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableCaching
public class SiteServerApiConfiguration {

  @Value("${siteserver.api.latest.version}")
  private String latestApiVersion;

  @Value("${siteserver.priceboost.enabled}")
  private boolean isPriceBoostEnabled;

  @Value("${siteServer.api.version}")
  private String apiVersion;

  @Bean
  public SiteServerApi siteServerAPI( //
      @Value("${siteServer.base.url}") String siteServerUrl, //
      @Value("${siteServer.connection.timeout}") int connectionTimeout, //
      @Value("${siteServer.read.timeout}") int readTimeout, //
      @Value("${siteServer.retries.number}") int retriesNumber, //
      @Value("${siteServer.logging.level}") String loggingLevel //
      ) throws NoSuchAlgorithmException, KeyManagementException {
    return new SiteServerApi.Builder() //
        .setUrl(siteServerUrl) //
        .setLoggingLevel(SiteServerApi.Level.valueOf(loggingLevel)) //
        .setConnectionTimeout(connectionTimeout) //
        .setReadTimeout(readTimeout) //
        .setMaxNumberOfRetries(retriesNumber) //
        .setVersion(getapiVersion()) //
        .build();
  }

  private String getapiVersion() {
    if (isPriceBoostEnabled) {
      return latestApiVersion;
    }
    return apiVersion;
  }
}
