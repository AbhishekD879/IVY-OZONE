package com.coral.oxygen.middleware.common.configuration;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@Setter
public class SiteServerAPIConfiguration {

  @Value("${siteServer.base.url}")
  private String baseUrl;

  @Value("${siteServer.logging.level}")
  private String level;

  @Value("${siteServer.connection.timeout}")
  private int connectionTimeout;

  @Value("${siteServer.read.timeout}")
  private int readTimeout;

  @Value("${siteServer.retries.number}")
  private int retriesNumber;

  @Value("${siteServer.pool.size}")
  private int poolSize;

  @Value("${siteServer.keep.alive.seconds}")
  private long keepAliveSeconds;

  @Value("${siteServer.api.version}")
  private String apiVersion;

  @Value("${siteServer.api.latest.version}")
  private String latestApiVersion;

  @Value("${siteServer.priceboost.enabled}")
  private boolean isPriceBoostEnabled;

  @Bean
  public SiteServerApi getSiteServerAPI() throws KeyManagementException, NoSuchAlgorithmException {
    return new SiteServerApi.Builder()
        .setUrl(baseUrl)
        .setVersion(latestApiVersion)
        .setLoggingLevel(SiteServerApi.Level.valueOf(level))
        .setConnectionTimeout(connectionTimeout)
        .setReadTimeout(readTimeout)
        .setConnectionPoolSettings(poolSize, keepAliveSeconds)
        .setMaxNumberOfRetries(retriesNumber)
        .build();
  }
}
