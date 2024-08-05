package com.ladbrokescoral.oxygen.configuration;

import com.ladbrokescoral.oxygen.utils.EnvironmentProvider;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;

@Configuration
@PropertySource("classpath:git.properties")
public class EnvironmentProviderConfiguration {

  @Bean
  public EnvironmentProvider gitPropertiesResolver(Environment env) {
    return new EnvironmentProvider(env);
  }
}
