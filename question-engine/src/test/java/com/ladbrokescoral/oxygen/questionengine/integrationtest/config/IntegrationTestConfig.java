package com.ladbrokescoral.oxygen.questionengine.integrationtest.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import uk.co.jemos.podam.api.PodamFactory;
import uk.co.jemos.podam.api.PodamFactoryImpl;

@Configuration
public class IntegrationTestConfig {

  @Bean
  public PodamFactory podamFactory() {
    return new PodamFactoryImpl();
  }
}
