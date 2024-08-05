package com.ladbrokescoral.oxygen.timeline.api.controller;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.atLeastOnce;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.timeline.api.model.message.CampaignMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.message.Message;
import com.ladbrokescoral.oxygen.timeline.api.service.MessageProcessor;
import com.ladbrokescoral.oxygen.timeline.api.service.impl.CampaignMessageProcessor;
import java.time.Instant;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.*;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.kafka.core.reactive.ReactiveKafkaConsumerTemplate;
import reactor.core.publisher.Flux;

@RunWith(MockitoJUnitRunner.class)
public class MessageListenerTest {
  @InjectMocks MessageListener messageListener;
  @Mock private ReactiveKafkaConsumerTemplate<String, Message> reactiveKafkaConsumerTemplate;
  @Mock MessageProcessorFactory messageProcessorFactory;

  @Test
  public void consumeTestOnError() throws Exception {
    Message campaignPostMessage =
        new CampaignMessage()
            .setDisplayFrom(Instant.parse("2023-05-03T10:20:29.016Z"))
            .setDisplayTo(Instant.parse("2023-05-30T10:20:29Z"))
            .setPageSize(5)
            .setId("6459e0beb473101c8def8b0b")
            .setCreatedDate(Instant.parse("2023-05-09T06:00:01.895404900Z"))
            .setBrand("ladbrokes");
    ConsumerRecord<String, Message> record =
        new ConsumerRecord<>("timeline", 0, 0, "", campaignPostMessage);
    when(reactiveKafkaConsumerTemplate.receiveAutoAck()).thenReturn(Flux.just(record));
    messageListener.run();
    Mockito.verify(messageProcessorFactory, atLeastOnce()).getInstance(any());
  }

  @Test
  public void consumeTest() throws Exception {
    MessageProcessor processor = Mockito.mock(CampaignMessageProcessor.class);
    Message campaignPostMessage =
        new CampaignMessage()
            .setDisplayFrom(Instant.parse("2023-05-03T10:20:29.016Z"))
            .setDisplayTo(Instant.parse("2023-05-30T10:20:29Z"))
            .setPageSize(5)
            .setId("6459e0beb473101c8def8b0b")
            .setCreatedDate(Instant.parse("2023-05-09T06:00:01.895404900Z"))
            .setBrand("ladbrokes");
    ConsumerRecord<String, Message> record =
        new ConsumerRecord<>("timeline", 0, 0, "", campaignPostMessage);
    when(reactiveKafkaConsumerTemplate.receiveAutoAck()).thenReturn(Flux.just(record));
    when(messageProcessorFactory.getInstance(any(Class.class))).thenReturn(processor);
    messageListener.run();
    Mockito.verify(messageProcessorFactory, atLeastOnce()).getInstance(any());
  }
}
