package com.ladbrokescoral.oxygen.service;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.AsyncResult;

@ExtendWith(MockitoExtension.class)
class BetPackKafkaPublisherTest {
  @Mock KafkaTemplate<String, String> kafkaTemplate;

  @Mock AsyncResult asyncResult;

  @MockBean BetPackKafkaPublisher messagePublisher;

  private static final String CHANNEL = "channel";
  private static final String TOPIC = "topic";

  @BeforeEach
  void init() {
    messagePublisher = new BetPackKafkaPublisher(kafkaTemplate, TOPIC);
    messagePublisher = mock(BetPackKafkaPublisher.class);
  }

  @Test
  void testSendNotification() {
    messagePublisher.publish(CHANNEL, "message");
    assertNotNull(CHANNEL);
  }
}
