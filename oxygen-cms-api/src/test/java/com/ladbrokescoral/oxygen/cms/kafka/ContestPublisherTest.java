package com.ladbrokescoral.oxygen.cms.kafka;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.util.concurrent.SettableListenableFuture;

@ExtendWith(MockitoExtension.class)
@Slf4j
class ContestPublisherTest {

  @Mock private KafkaTemplate<String, String> kafkaTemplate;

  @Test
  void publish_Test() {
    ContestPublisher responsePublisher = new ContestPublisher(kafkaTemplate, "leaderboard-contest");
    Map<String, String> map = new HashMap<>();
    map.put("topic", "leaderboard-contest");

    SettableListenableFuture<SendResult<String, String>> future = new SettableListenableFuture<>();

    RecordMetadata recordMetadata = new RecordMetadata(null, 1l, 2l, 3l, 4l, 1, 2);
    SendResult<String, String> result =
        new SendResult<>(new ProducerRecord("a", null), recordMetadata);
    future.set(result);

    Mockito.when(kafkaTemplate.send((ProducerRecord<String, String>) Mockito.any()))
        .thenReturn(future);
    responsePublisher.publish("key", "requestMsg", Optional.of(map));
    verify(kafkaTemplate, times(1)).send((ProducerRecord<String, String>) Mockito.any());
  }

  @Test
  void publish_Test_Exception() {
    ContestPublisher responsePublisher = new ContestPublisher(kafkaTemplate, "leaderboard-contest");
    Map<String, String> map = new HashMap<>();
    map.put("topic", "leaderboard-contest");

    SettableListenableFuture<SendResult<String, String>> future = new SettableListenableFuture<>();

    future.setException(new Throwable());

    Mockito.when(kafkaTemplate.send((ProducerRecord<String, String>) Mockito.any()))
        .thenReturn(future);
    responsePublisher.publish("key", "requestMsg", Optional.of(map));
    verify(kafkaTemplate, times(1)).send((ProducerRecord<String, String>) Mockito.any());
  }
}
