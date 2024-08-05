package com.coral.oxygen.middleware.in_play.service.config;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.integration.dsl.MessageChannels;
import org.springframework.messaging.SubscribableChannel;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@Configuration
public class SubscriptionConfig {

  @Bean
  public SubscribableChannel messageChannel(
      @Qualifier("threadPoolTaskExecutor") ThreadPoolTaskExecutor threadPoolTaskExecutor) {
    return MessageChannels.publishSubscribe("springIntegrationPubSub", threadPoolTaskExecutor)
        .get();
  }
}
