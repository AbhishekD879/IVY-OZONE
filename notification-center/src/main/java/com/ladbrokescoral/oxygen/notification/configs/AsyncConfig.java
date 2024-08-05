package com.ladbrokescoral.oxygen.notification.configs;

import java.util.concurrent.Executor;
import java.util.concurrent.Executors;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;

/** This is used to provide async executor for kafka message processing. */
@Configuration
@EnableAsync
public class AsyncConfig {

  public static final String EXECUTOR_QUALIFIER_KAFKA = "threadPoolTaskExecutorKafkaUpdates";

  @Bean(name = EXECUTOR_QUALIFIER_KAFKA)
  public Executor threadPoolTaskExecutor(
      @Value("${kafka.handler.scheduled-pool-core-size}") int corePoolSize) {
    return Executors.newScheduledThreadPool(corePoolSize);
  }
}
