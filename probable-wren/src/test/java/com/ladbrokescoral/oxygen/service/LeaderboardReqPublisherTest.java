package com.ladbrokescoral.oxygen.service;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import java.util.HashMap;
import java.util.Map;
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
class LeaderboardReqPublisherTest {
  @Mock private KafkaTemplate<String, String> kafkaTemplate;

  @Test
  void publish_Test() {
    LeaderboardReqPublisher responsePublisher =
        new LeaderboardReqPublisher(kafkaTemplate, "showdown-request-topic");
    Map<String, String> map = new HashMap<>();
    map.put("topic", "leaderboard-contest");

    SettableListenableFuture<SendResult<String, String>> future = new SettableListenableFuture<>();

    RecordMetadata recordMetadata = new RecordMetadata(null, 1l, 2l, 3l, 4l, 1, 2);
    SendResult<String, String> result =
        new SendResult<>(new ProducerRecord("a", null), recordMetadata);
    future.set(result);

    Mockito.when(kafkaTemplate.send(Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(future);
    responsePublisher.publish("key", "requestMsg");
    verify(kafkaTemplate, times(0)).send((ProducerRecord<String, String>) Mockito.any());
  }

  @Test
  void publish_Test_Exception() {
    LeaderboardReqPublisher responsePublisher =
        new LeaderboardReqPublisher(kafkaTemplate, "showdown-request-topic");
    Map<String, String> map = new HashMap<>();
    map.put("topic", "leaderboard-contest");

    SettableListenableFuture<SendResult<String, String>> future = new SettableListenableFuture<>();

    future.setException(new Throwable());

    Mockito.when(kafkaTemplate.send(Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(future);
    responsePublisher.publish("key", "requestMsg");
    verify(kafkaTemplate, times(0)).send((ProducerRecord<String, String>) Mockito.any());
  }
}
