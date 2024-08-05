package com.coral.oxygen.middleware.ms.liveserv.impl.kafka;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class KafkaScoreboardsPublisher extends AbstractKafkaPublisher {

  public KafkaScoreboardsPublisher(
      KafkaTemplate<String, String> kafkaTemplate, @Value("${topic.scoreboards}") String topic) {
    super(kafkaTemplate, topic);
  }
}
