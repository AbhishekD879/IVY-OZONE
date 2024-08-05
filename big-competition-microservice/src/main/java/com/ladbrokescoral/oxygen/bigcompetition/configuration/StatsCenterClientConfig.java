package com.ladbrokescoral.oxygen.bigcompetition.configuration;

import com.ladbrokescoral.oxygen.betradar.client.service.StatsCenterApiClient;
import com.ladbrokescoral.oxygen.betradar.client.service.StatsCenterApiClientImpl;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class StatsCenterClientConfig {

  @Bean
  public StatsCenterApiClient statsCenterApiClient(
      @Value("${stats.center.url}") String statsCenterBaseUrl) {
    return new StatsCenterApiClientImpl(statsCenterBaseUrl);
  }
}
