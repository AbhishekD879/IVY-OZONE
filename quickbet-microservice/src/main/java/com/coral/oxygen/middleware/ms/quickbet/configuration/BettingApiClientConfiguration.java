package com.coral.oxygen.middleware.ms.quickbet.configuration;

import com.entain.oxygen.bettingapi.service.BettingOptions;
import com.entain.oxygen.bettingapi.service.BettingService;
import com.entain.oxygen.bettingapi.service.BettingServiceFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class BettingApiClientConfiguration {
  @Bean
  public BettingService bettingService(
      @Value("${betting-api.url}") String bettingApiUrl,
      @Value("${betting-api.read.timeout}") int bettingApiReadTimeout,
      @Value("${betting-api.connect.timeout}") int bettingApiConnectTimeout) {
    return BettingServiceFactory.createWithOptions(
        BettingOptions.builder()
            .baseUrl(bettingApiUrl)
            .connectTimeout(bettingApiConnectTimeout)
            .readTimeout(bettingApiReadTimeout)
            .retryCount(0)
            .build());
  }
}
