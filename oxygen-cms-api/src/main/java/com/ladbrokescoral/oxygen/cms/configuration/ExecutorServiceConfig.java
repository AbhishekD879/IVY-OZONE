package com.ladbrokescoral.oxygen.cms.configuration;

import com.ladbrokescoral.oxygen.cms.util.CustomExecutors;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ExecutorServiceConfig {

  @Bean
  public ExecutorService cachedThreadPool() {
    return Executors.newCachedThreadPool();
  }

  @Bean
  public CustomExecutors customExecutors() {
    return new CustomExecutors();
  }
}
