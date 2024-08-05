package com.oxygen.publisher.sportsfeatured.configuration;

import com.oxygen.publisher.service.CallExecutorService;
import com.oxygen.publisher.sportsfeatured.service.SportsChainFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Created by Aliaksei Yarotski on 2/5/18. */
@Configuration
public class CallExecutorServiceConfiguration {

  @Bean
  public CallExecutorService callExecutor(
      SportsChainFactory featuredChainFactory, @Value("${tt.job.rate}") long waitForJobRun) {
    return new CallExecutorService(featuredChainFactory, waitForJobRun);
  }
}
