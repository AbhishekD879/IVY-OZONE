package com.oxygen.publisher.inplay.configuration;

import com.oxygen.publisher.inplay.service.InplayChainFactory;
import com.oxygen.publisher.service.CallExecutorService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Created by Aliaksei Yarotski on 2/5/18. */
@Configuration
public class CallExecutorServiceConfiguration {

  @Bean
  public CallExecutorService callExecutor(
      InplayChainFactory inplayChainFactory, @Value("${tt.cache.minute}") long waitForJobRun) {
    return new CallExecutorService(inplayChainFactory, waitForJobRun * 60);
  }
}
