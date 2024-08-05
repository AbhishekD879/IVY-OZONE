package com.oxygen.publisher.sportsfeatured.configuration;

import com.oxygen.publisher.sportsfeatured.SportsServiceRegistry;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Created by Aliaksei Yarotski on 1/11/18. */
@Configuration
public class ServiceRegistryConfiguration {

  @Bean
  public SportsServiceRegistry medianServiceRegistry(ConfigurableApplicationContext appContext) {
    return new SportsServiceRegistry(appContext);
  }
}
