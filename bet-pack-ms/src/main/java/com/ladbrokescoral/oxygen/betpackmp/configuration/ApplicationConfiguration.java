package com.ladbrokescoral.oxygen.betpackmp.configuration;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ApplicationConfiguration {

  @Bean
  @Qualifier("distributedPrefix")
  public String distributedPrefix(@Value("${distributed.prefix}") String prefix) {
    return prefix;
  }
}
