package com.coral.oxygen.middleware.ms.quickbet.configuration;

import java.util.concurrent.ScheduledThreadPoolExecutor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OveraskReadBetConfiguration {
  @Value("${overask.readBet.retry.initialDelay.millis}")
  private Long defaultInitialDelay;

  @Value("${overask.readBet.retry.delay.millis}")
  private Long retryDelay;

  @Value("${overask.readBet.retry.maxNumberOfRetries}")
  private Integer maxNumberOfRetries;

  @Value("${overask.readBet.threadPool.size}")
  private Integer threadPoolSize;

  public Long getDefaultInitialDelay() {
    return defaultInitialDelay;
  }

  public Long getRetryDelay() {
    return retryDelay;
  }

  public Integer getMaxNumberOfRetries() {
    return maxNumberOfRetries;
  }

  @Bean
  public ScheduledThreadPoolExecutor scheduledThreadPoolExecutor() {
    return new ScheduledThreadPoolExecutor(threadPoolSize);
  }
}
