package com.oxygen.publisher.inplay.configuration;

import com.oxygen.publisher.inplay.InplayServiceRegistry;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Created by Aliaksei Yarotski on 1/11/18. */
@Configuration
public class ServiceRegistryConfiguration {

  @Bean
  public InplayServiceRegistry medianServiceRegistry(ConfigurableApplicationContext appContext) {
    return new InplayServiceRegistry(appContext);
  }
}
