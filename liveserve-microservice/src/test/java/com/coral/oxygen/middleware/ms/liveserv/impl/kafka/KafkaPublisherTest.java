package com.coral.oxygen.middleware.ms.liveserv.impl.kafka;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.AsyncResult;

@RunWith(MockitoJUnitRunner.class)
public class KafkaPublisherTest {

  @Mock KafkaTemplate<String, String> kafkaTemplate;

  @Mock AsyncResult asyncResult;

  KafkaUpdatePublisher messagePublisher;

  private static final String CHANNEL = "channel";
  private static final String MESSAGE = "message";
  private static final String TOPIC = "topic";

  @Before
  public void init() {
    messagePublisher = new KafkaUpdatePublisher(kafkaTemplate, TOPIC);
    when(kafkaTemplate.send(any(), any(), any())).thenReturn(asyncResult);
  }

  @Test
  public void testSendNotification() {
    messagePublisher.publish(CHANNEL, MESSAGE);
    verify(kafkaTemplate, times(1)).send(TOPIC, CHANNEL, MESSAGE);
  }
}
