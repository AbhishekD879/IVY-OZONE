package com.coral.oxygen.middleware.ms.quickbet.configuration;

import com.coral.bpp.api.service.BppOptions;
import com.coral.bpp.api.service.BppService;
import com.coral.bpp.api.service.BppServiceFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class BppApiClientConfiguration {

  @Bean
  public BppService bppService(
      @Value("${bpp.url}") String bppUrl,
      @Value("${bpp.read.timeout}") int bppReadTimeout,
      @Value("${bpp.connect.timeout}") int bppConnectTimeout) {
    return BppServiceFactory.createWithOptions(
        BppOptions.builder()
            .baseUrl(bppUrl)
            .connectTimeout(bppConnectTimeout)
            .readTimeout(bppReadTimeout)
            .retryCount(0)
            .build());
  }
}
