package com.ladbrokescoral.oxygen.service;

import lombok.Setter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
@Setter
public class LeaderboardReqPublisher extends AbstractKafkaPublisher {

  public LeaderboardReqPublisher(
      KafkaTemplate<String, String> kafkaTemplate,
      @Value("${topic.showdown.request}") String topic) {
    super(kafkaTemplate, topic);
  }
}
