package com.oxygen.publisher.inplay.configuration;

import com.oxygen.publisher.inplay.InplayHealthIndicator;
import com.oxygen.publisher.inplay.InplayServiceRegistry;
import com.oxygen.publisher.inplay.context.InplayMiddlewareContext;
import com.oxygen.publisher.inplay.context.InplaySessionContext;
import com.oxygen.publisher.inplay.service.InplayDataService;
import com.oxygen.publisher.inplay.service.InplayDataServiceImpl;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class InplayServiceConfiguration {

  @Bean
  public InplayDataService inplayDataService(InplayServiceRegistry serviceRegistry) {
    InplayDataServiceImpl service = new InplayDataServiceImpl();
    service.setServiceRegistry(serviceRegistry);
    return service;
  }

  @Bean
  public InplayMiddlewareContext middlewareContext(InplayServiceRegistry serviceRegistry) {
    return new InplayMiddlewareContext(serviceRegistry);
  }

  @Bean
  public InplaySessionContext featuredSessionContext(
      @Value("${publisher.version}") String appVersion,
      InplayMiddlewareContext inplayMiddlewareContext) {
    return new InplaySessionContext(appVersion, inplayMiddlewareContext);
  }

  @Bean
  public InplayHealthIndicator inplayHealthIndicator(
      InplayMiddlewareContext inplayMiddlewareContext, InplayServiceRegistry serviceRegistry) {
    return new InplayHealthIndicator(inplayMiddlewareContext, serviceRegistry);
  }
}
