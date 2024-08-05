package com.coral.oxygen.middleware.common.configuration;

import com.coral.oxygen.middleware.common.service.notification.topic.TopicResolver;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DistributedKafkaConfig {

  @Value("${distributed.prefix}")
  private String distributedPrefix;

  @Bean
  public TopicResolver topicResolver() {
    return new TopicResolver(distributedPrefix);
  }
}
