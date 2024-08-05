package com.ladbrokescoral.oxygen.cms.configuration;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.entity.StreamAndBetShortNode;
import com.ladbrokescoral.oxygen.cms.api.exception.SiteServeApiInitializationException;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.IOUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Slf4j
@Configuration
public class SiteServerApiConfiguration {

  @Value("${siteserver.base.url}")
  private String siteServerUrl;

  @Value("${siteserver.api.version}")
  private String apiVersion;

  @Value("${siteserver.api.latest.version}")
  private String latestApiVersion;

  @Value("${siteserver.priceboost.enabled}")
  private boolean isPriceBoostEnabled;

  @Value("${siteserver.connection.timeout}")
  private int connectionTimeout;

  @Value("${siteserver.read.timeout}")
  private int readTimeout;

  @Value("${siteserver.retries.number}")
  private int retriesNumber;

  @Value("${siteserver.logging.level}")
  private String loggingLevel;

  /** @return SiteServerApi with default url */
  public SiteServerApi siteServerAPI() {
    return siteServerAPI(this.siteServerUrl);
  }

  /** @return SiteServerApi with specified siteServe url */
  public SiteServerApi siteServerAPI(String siteServerUrl) {
    try {
      return new SiteServerApi.Builder()
          .setUrl(siteServerUrl)
          .setLoggingLevel(SiteServerApi.Level.valueOf(loggingLevel))
          .setConnectionTimeout(connectionTimeout)
          .setReadTimeout(readTimeout)
          .setMaxNumberOfRetries(retriesNumber)
          .setVersion(getapiVersion())
          .build();
    } catch (NoSuchAlgorithmException | KeyManagementException e) {
      log.error("Error initializing SiteServerApi", e);
      throw new SiteServeApiInitializationException();
    }
  }

  @Bean
  public List<StreamAndBetShortNode> getCategoriesList() {
    ObjectMapper mapper = new ObjectMapper();
    try {
      List<StreamAndBetShortNode> nodeList =
          mapper.readValue(
              IOUtils.resourceToString("/configuration/categories.json", StandardCharsets.UTF_8),
              new TypeReference<List<StreamAndBetShortNode>>() {});
      nodeList.sort(Comparator.comparing(StreamAndBetShortNode::getName));
      return nodeList;
    } catch (IOException e) {
      log.error("categories.json doesn`t exist", e);
    }
    return Collections.emptyList();
  }

  /** @return default siteServe */
  public String getSiteServerUrl() {
    return siteServerUrl;
  }

  private String getapiVersion() {
    if (isPriceBoostEnabled) {
      return latestApiVersion;
    }
    return apiVersion;
  }
}
