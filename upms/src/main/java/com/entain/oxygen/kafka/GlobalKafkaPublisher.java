package com.entain.oxygen.kafka;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class GlobalKafkaPublisher extends AbstractKafkaPublisher {

  public GlobalKafkaPublisher(
      KafkaTemplate<String, String> globalKafkaTemplate,
      @Value("${rtms.kafka.rtms-publisher}") String topic) {
    super(globalKafkaTemplate, topic);
  }
}
