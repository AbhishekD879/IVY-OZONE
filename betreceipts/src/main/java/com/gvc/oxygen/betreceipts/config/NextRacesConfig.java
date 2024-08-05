package com.gvc.oxygen.betreceipts.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class NextRacesConfig {

  @Bean
  @ConfigurationProperties(prefix = "app.next-races")
  public NextRaceProps nextRaceProps() {
    return new NextRaceProps();
  }
}
