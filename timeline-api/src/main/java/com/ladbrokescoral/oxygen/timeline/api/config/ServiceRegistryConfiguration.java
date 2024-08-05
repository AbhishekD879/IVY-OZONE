package com.ladbrokescoral.oxygen.timeline.api.config;

import com.ladbrokescoral.oxygen.timeline.api.registrators.TimelineServiceRegistry;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ServiceRegistryConfiguration {

  @Bean
  public TimelineServiceRegistry medianServiceRegistry(ConfigurableApplicationContext appContext) {
    return new TimelineServiceRegistry(appContext);
  }
}
