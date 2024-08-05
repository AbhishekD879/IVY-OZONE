package com.entain.oxygen.kafka;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.util.concurrent.SettableListenableFuture;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class AbstractKafkaPublisherTest {

  @Mock private KafkaTemplate<String, String> kafkaTemplate;
  private String topic = "AbstractTopic";

  @Test
  void publish_Test() {
    AbstractKafkaPublisher abstractKafkaPublisher =
        new AbstractKafkaPublisher(kafkaTemplate, "AbstractTopic");
    Map<String, String> map = new HashMap<>();
    map.put("topic", "AbstractTopic");

    SettableListenableFuture<SendResult<String, String>> future = new SettableListenableFuture<>();
    RecordMetadata recordMetadata = new RecordMetadata(null, 1l, 2l, 3l, 4l, 1, 2);
    SendResult<String, String> result =
        new SendResult<>(new ProducerRecord("a", null), recordMetadata);
    Mockito.when(kafkaTemplate.send((ProducerRecord<String, String>) Mockito.any()))
        .thenReturn(future);
    abstractKafkaPublisher.publishMessage("key", "requestMsg", Optional.of(map));
    verify(kafkaTemplate, times(1)).send((ProducerRecord<String, String>) Mockito.any());
  }
}
