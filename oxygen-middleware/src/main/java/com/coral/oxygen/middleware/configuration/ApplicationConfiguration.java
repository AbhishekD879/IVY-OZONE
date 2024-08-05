package com.coral.oxygen.middleware.configuration;

import com.coral.oxygen.middleware.util.PropertyUtils;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Properties;
import java.util.Set;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.ConfigurableEnvironment;

@Slf4j
@Configuration
public class ApplicationConfiguration {

  @Value("${app.version}")
  private String appVersion;

  @Bean(name = "ApplicationConfiguration")
  public ApplicationConfiguration initConfiguration(ConfigurableEnvironment environment) {

    Properties properties = PropertyUtils.getProperties(environment);
    Set<Entry<Object, Object>> set = properties.entrySet();
    log.info("Application version {}", appVersion);
    log.info("Application properties :");
    for (Map.Entry<Object, Object> object : set) {
      log.info("Application Property {}={}", object.getKey(), object.getValue());
    }

    return this;
  }
}
