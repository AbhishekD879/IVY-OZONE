package com.oxygen.publisher.sportsfeatured.configuration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.oxygen.publisher.sportsfeatured.context.SportsMiddlewareContext;
import com.oxygen.publisher.sportsfeatured.context.SportsSessionContext;
import com.oxygen.publisher.sportsfeatured.service.SportsChainFactory;
import com.oxygen.publisher.translator.DiagnosticService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Created by Aliaksei Yarotski on 12/29/17. */
@Slf4j
@Configuration
public class WorkersConfiguration {

  @Bean
  public SportsChainFactory createFeaturedChainFactory(
      SportsMiddlewareContext featuredMiddlewareContext,
      ObjectMapper objectMapper,
      DiagnosticService diagnosticService,
      SportsSessionContext sportsSessionContext) {
    SportsChainFactory.setFeaturedChainFactory(
        new SportsChainFactory(
            featuredMiddlewareContext, objectMapper, diagnosticService, sportsSessionContext));

    return SportsChainFactory.getFeaturedChainFactory();
  }
}
