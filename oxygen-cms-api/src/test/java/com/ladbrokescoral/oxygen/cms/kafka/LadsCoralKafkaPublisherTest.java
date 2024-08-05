package com.ladbrokescoral.oxygen.cms.kafka;

import static org.mockito.Mockito.*;

import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.util.concurrent.SettableListenableFuture;

@ExtendWith(MockitoExtension.class)
@Slf4j
class LadsCoralKafkaPublisherTest {

  @Mock private KafkaTemplate<String, String> coralkafkaTemplate;
  @Mock private KafkaTemplate<String, String> ladbrokesKafkaTemplate;

  @Test
  void publish_Test() {
    LadsCoralKafkaPublisher responsePublisher =
        new LadsCoralKafkaPublisher(coralkafkaTemplate, ladbrokesKafkaTemplate);
    SettableListenableFuture<SendResult<String, String>> future = new SettableListenableFuture<>();

    RecordMetadata recordMetadata = new RecordMetadata(null, 1l, 2l, 3l, 4l, 1, 2);
    SendResult<String, String> result =
        new SendResult<>(new ProducerRecord("a", null), recordMetadata);
    future.set(result);
    when(coralkafkaTemplate.send("a", "bma", "ccc")).thenReturn(future);
    responsePublisher.publishMessage("a", "bma", "ccc");
    verify(coralkafkaTemplate, times(1)).send("a", "bma", "ccc");
  }

  @Test
  void publish_ExceptionTest() {
    LadsCoralKafkaPublisher responsePublisher =
        new LadsCoralKafkaPublisher(coralkafkaTemplate, ladbrokesKafkaTemplate);
    SettableListenableFuture<SendResult<String, String>> future = new SettableListenableFuture<>();

    future.setException(new Throwable());
    when(coralkafkaTemplate.send("a", "bma", "ccc")).thenReturn(future);
    responsePublisher.publishMessage("a", "bma", "ccc");
    verify(coralkafkaTemplate, times(1)).send("a", "bma", "ccc");
  }

  @Test
  void publish_ExceptionTestlad() {
    LadsCoralKafkaPublisher responsePublisher =
        new LadsCoralKafkaPublisher(coralkafkaTemplate, ladbrokesKafkaTemplate);
    SettableListenableFuture<SendResult<String, String>> future = new SettableListenableFuture<>();

    future.setException(new Throwable());
    when(ladbrokesKafkaTemplate.send("a", "lad", "ccc")).thenReturn(future);
    responsePublisher.publishMessage("a", "lad", "ccc");
    verify(ladbrokesKafkaTemplate, times(1)).send("a", "lad", "ccc");
  }
}
