package com.entain.oxygen.kafka;

import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;

@ExtendWith(MockitoExtension.class)
class KafkaPublisherTest implements WithAssertions {

  @Mock private KafkaTemplate<String, String> kafkaTemplate;

  @InjectMocks private GlobalKafkaPublisher kafkaPublisher;

  @Test
  void kafkaBetPacksPublisherTest() {
    kafkaPublisher = new GlobalKafkaPublisher(kafkaTemplate, "kafka_topic");
    Assertions.assertNotNull(kafkaPublisher);
  }
}
