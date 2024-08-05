package com.coral.oxygen.edp.configuration;

import com.coral.oxygen.df.api.DFClient;
import com.coral.oxygen.df.api.impl.DFClientImpl;
import com.coral.oxygen.df.api.impl.DFHttpClient;
import com.coral.oxygen.edp.exceptions.DFApiInitializationException;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import okhttp3.logging.HttpLoggingInterceptor.Level;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Slf4j
@Configuration
@ConfigurationProperties(prefix = "df")
@Data
public class DFApiConfig {

  private String baseUrl;

  private String apiKey = "PleaseSetCorrectApiKey";

  private String apiVersion;

  private int connectionTimeout;

  private int readTimeout;

  private int retriesNumber;

  private String loggingLevel;

  /**
   * @return DfApi with specified df api url
   */
  public DFClient api() {
    try {
      log.info("DFApiConfig constructor called");
      DFHttpClient dfHttpClient =
          DFHttpClient.builder()
              .loggerLevel(Level.valueOf(loggingLevel))
              .connectTimeout(connectionTimeout)
              .readTimeout(readTimeout)
              .build();

      return DFClientImpl.builder()
          .baseUrl(baseUrl, dfHttpClient.getHttpClient())
          .maxNumberOfRetries(retriesNumber)
          .version(apiVersion)
          .apiKey(apiKey)
          .build();

    } catch (NoSuchAlgorithmException | KeyManagementException e) {
      log.error("Error initializing DF API from EDP", e);
      throw new DFApiInitializationException(e);
    }
  }
}
