package com.coral.oxygen.middleware.common.configuration;

import com.coral.oxygen.middleware.common.service.notification.KafkaPublisher;
import com.coral.oxygen.middleware.common.service.notification.MessagePublisher;
import com.coral.oxygen.middleware.common.service.notification.topic.TopicResolver;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.KafkaTemplate;

@Configuration
@RequiredArgsConstructor
public class MessagePublisherConfiguration {

  private final KafkaTemplate<String, String> kafkaTemplate;
  private final TopicResolver topicResolver;

  @Bean
  MessagePublisher kafkaMessageProducer() {
    return new KafkaPublisher(kafkaTemplate, topicResolver);
  }
}
