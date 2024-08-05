package com.ladbrokescoral.oxygen.cms.kafka;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class ContestPublisher extends AbstractKafkaPublisher {
  public ContestPublisher(
      KafkaTemplate<String, String> ladbrokesKafkaTemplate,
      @Value("${ladbrokes.kafka.topic.leaderboard-contest}") String topic) {
    super(ladbrokesKafkaTemplate, topic);
  }
}
