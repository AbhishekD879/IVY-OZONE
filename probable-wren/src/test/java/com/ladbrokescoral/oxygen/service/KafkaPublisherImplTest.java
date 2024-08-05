package com.ladbrokescoral.oxygen.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.AsyncResult;

@ExtendWith(MockitoExtension.class)
public class KafkaPublisherImplTest {
  @Mock KafkaTemplate<String, String> kafkaTemplate;

  @Mock AsyncResult asyncResult;

  KafkaPublisherImpl messagePublisher;

  private static final String CHANNEL = "channel";
  private static final String TOPIC = "topic";

  @BeforeEach
  public void init() {
    messagePublisher = new KafkaPublisherImpl(kafkaTemplate, TOPIC);
    messagePublisher.publish(CHANNEL, "message");
    when(kafkaTemplate.send(anyString(), any(), any())).thenReturn(asyncResult);
  }

  @Test
  @Disabled
  public void testSendNotification() {
    messagePublisher.publish(CHANNEL, null);
    verify(kafkaTemplate, times(1)).send(TOPIC, CHANNEL, "message");
  }
}
