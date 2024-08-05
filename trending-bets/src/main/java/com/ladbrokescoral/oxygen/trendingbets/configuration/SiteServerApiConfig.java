package com.ladbrokescoral.oxygen.trendingbets.configuration;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.api.SiteServerApiAsync;
import com.egalacoral.spark.siteserver.api.SiteServerAsyncImpl;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import lombok.Data;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import reactor.netty.http.client.HttpClient;

@ConfigurationProperties(prefix = "site-server")
@Data
@Configuration
public class SiteServerApiConfig {

  private static final int MAX_MEMORY_SIZE = 2 * 1024 * 1024;

  @Bean
  public SiteServerApi siteServerAPI(
      @Value("${siteServer.baseUrl}") String baseUrl,
      @Value("${siteServer.apiVersion}") String apiVersion,
      @Value("${siteServer.loggingLevel}") String loggingLevel,
      @Value("${siteServer.connectionTimeout}") int connectionTimeout,
      @Value("${siteServer.readTimeout}") int readTimeout,
      @Value("${siteServer.retriesNumber}") int retriesNumber)
      throws NoSuchAlgorithmException, KeyManagementException {
    return new SiteServerApi.Builder()
        .setUrl(baseUrl)
        .setLoggingLevel(SiteServerApi.Level.valueOf(loggingLevel))
        .setConnectionTimeout(connectionTimeout)
        .setReadTimeout(readTimeout)
        .setMaxNumberOfRetries(retriesNumber)
        .setVersion(apiVersion)
        .build();
  }

  @Bean
  public SiteServerApiAsync siteServerApiAsync(
      @Value("${siteServer.baseUrl}") String baseUrl,
      @Value("${siteServer.apiVersion}") String apiVersion,
      HttpClient defaultClient) {
    return new SiteServerAsyncImpl(
        baseUrl, apiVersion, new ReactorClientHttpConnector(defaultClient), MAX_MEMORY_SIZE);
  }
}
