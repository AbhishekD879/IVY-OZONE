package com.coral.oxygen.middleware.ms.liveserv.impl.kafka;

import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.liveserv.model.messages.EventMessageEnvelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve.Message;
import com.google.gson.GsonBuilder;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class KafkaTopicMessageTest {

  @Mock private KafkaUpdatePublisher kafkaPublisher;

  private KafkaTopicMessageHandler kafkaTopicMessageHandler;

  @Before
  public void init() {
    kafkaTopicMessageHandler =
        new KafkaTopicMessageHandler(new GsonBuilder().create(), kafkaPublisher);
  }

  @Test
  public void handleTest() {
    EventMessageEnvelope envelope = new MessageEnvelope("channel", 1, new Message());
    kafkaTopicMessageHandler.handle(envelope);
    verify(kafkaPublisher, times(1)).publish(eq("1"), anyString());
  }
}
