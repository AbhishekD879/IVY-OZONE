package com.coral.oxygen.middleware.ms.liveserv.impl.kafka;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class KafkaIncidentsPublisher extends AbstractKafkaPublisher {

  /**
   * This Method is used to send VAR Messages into Internal Kafaka to LS Publisher
   *
   * @param kafkaTemplate
   * @param topic
   */
  public KafkaIncidentsPublisher(
      KafkaTemplate<String, String> kafkaTemplate, @Value("${topic.incidents}") String topic) {
    super(kafkaTemplate, topic);
  }
}
