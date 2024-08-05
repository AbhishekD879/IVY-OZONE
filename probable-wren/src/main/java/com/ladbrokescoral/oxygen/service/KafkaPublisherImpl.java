package com.ladbrokescoral.oxygen.service;

import lombok.Setter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
@Setter
public class KafkaPublisherImpl extends AbstractKafkaPublisher {

  public KafkaPublisherImpl(
      KafkaTemplate<String, String> kafkaTemplate, @Value("${topic.subscription}") String topic) {
    super(kafkaTemplate, topic);
  }
}
