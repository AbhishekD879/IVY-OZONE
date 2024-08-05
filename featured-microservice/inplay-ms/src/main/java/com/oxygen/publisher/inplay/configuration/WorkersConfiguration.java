package com.oxygen.publisher.inplay.configuration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.oxygen.publisher.inplay.context.InplayMiddlewareContext;
import com.oxygen.publisher.inplay.service.InplayChainFactory;
import com.oxygen.publisher.translator.DiagnosticService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Created by Aliaksei Yarotski on 12/29/17. */
@Slf4j
@Configuration
public class WorkersConfiguration {

  @Bean
  public InplayChainFactory createFeaturedChainFactory(
      InplayMiddlewareContext inplayMiddlewareContext,
      DiagnosticService diagnosticService,
      ObjectMapper objectMapper) {
    InplayChainFactory inplayChainFactory =
        new InplayChainFactory(inplayMiddlewareContext, diagnosticService, objectMapper);
    InplayChainFactory.setInplayChainFactory(inplayChainFactory);
    return InplayChainFactory.getInplayChainFactory();
  }
}
