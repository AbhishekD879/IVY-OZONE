package com.coral.oxygen.middleware.ms.liveserv.impl.kafka;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class KafkaUpdatePublisher extends AbstractKafkaPublisher {

  public KafkaUpdatePublisher(
      KafkaTemplate<String, String> kafkaTemplate, @Value("${topic.live-updates}") String topic) {
    super(kafkaTemplate, topic);
  }
}
