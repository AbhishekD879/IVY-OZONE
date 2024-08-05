package com.ladbrokescoral.oxygen.bigcompetition.configuration;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
// @Slf4j
public class SiteServerAPIConfiguration {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Value("${siteserver.api.version}")
  private String apiVersion;

  @Value("${siteserver.api.latest.version}")
  private String latestApiVersion;

  @Value("${siteserver.priceboost.enabled}")
  private boolean isPriceBoostEnabled;

  @Bean
  public SiteServerApi getSiteServerAPI(
      @Value("${siteServer.base.url}") String baseUrl,
      @Value("${siteServer.logging.level}") String level,
      @Value("${siteServer.connection.timeout}") int connectionTimeout,
      @Value("${siteServer.read.timeout}") int readTimeout,
      @Value("${siteServer.retries.number}") int retriesNumber) {
    try {
      return new SiteServerApi.Builder()
          .setUrl(baseUrl)
          .setVersion(getapiVersion())
          .setLoggingLevel(SiteServerApi.Level.valueOf(level))
          .setConnectionTimeout(connectionTimeout)
          .setReadTimeout(readTimeout)
          .setMaxNumberOfRetries(retriesNumber)
          .build();
    } catch (KeyManagementException | NoSuchAlgorithmException e) {
      ASYNC_LOGGER.error("Error during build SS api", e);
      throw new IllegalStateException("Error during initialisation SS api");
    }
  }

  public String getapiVersion() {
    if (isPriceBoostEnabled) {
      return latestApiVersion;
    }
    return apiVersion;
  }
}
