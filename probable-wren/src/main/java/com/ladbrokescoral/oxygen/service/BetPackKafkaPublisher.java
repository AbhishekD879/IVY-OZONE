package com.ladbrokescoral.oxygen.service;

import lombok.Setter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
@Setter
public class BetPackKafkaPublisher extends AbstractKafkaPublisher {

  public BetPackKafkaPublisher(
      KafkaTemplate<String, String> kafkaTemplate,
      @Value("${topic.bet-pack-subscription}") String topic) {
    super(kafkaTemplate, topic);
  }
}
