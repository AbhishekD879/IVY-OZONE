package com.ladbrokescoral.oxygen.cms.configuration;

import com.ladbrokescoral.oxygen.betradar.client.service.StatsCenterApiClient;
import com.ladbrokescoral.oxygen.betradar.client.service.StatsCenterApiClientImpl;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class StatsCenterClientConfig {

  @Value("${stats.center.url}")
  private String statsCenterBaseUrl;

  @Bean
  public StatsCenterApiClient statsCenterApiClient() {
    return new StatsCenterApiClientImpl(statsCenterBaseUrl);
  }
}
