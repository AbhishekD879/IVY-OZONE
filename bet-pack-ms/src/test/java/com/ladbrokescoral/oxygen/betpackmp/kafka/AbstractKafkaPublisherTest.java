package com.ladbrokescoral.oxygen.betpackmp.kafka;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.*;

import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetOffer;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.apache.kafka.common.TopicPartition;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.util.concurrent.ListenableFuture;
import org.springframework.util.concurrent.ListenableFutureCallback;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class AbstractKafkaPublisherTest {

  @Mock private KafkaTemplate<String, FreebetOffer> kafkaTemplate;

  @InjectMocks private AbstractKafkaPublisher abstractKafkaPublisher;

  private final String key = "key";
  private final String topic = "topic";
  private final long offset = 86876L;
  private final int partition = 3;

  @BeforeEach
  public void init() {
    abstractKafkaPublisher = new AbstractKafkaPublisher(kafkaTemplate, topic);
  }

  @Test
  void can_publishDataToKafka() {
    FreebetOffer freebetOffer = mock(FreebetOffer.class);
    SendResult<String, Object> sendResult = mock(SendResult.class);
    ListenableFuture<SendResult<String, FreebetOffer>> responseFuture =
        mock(ListenableFuture.class);
    RecordMetadata recordMetadata =
        new RecordMetadata(new TopicPartition(topic, partition), offset, 0L, 0L, 0L, 0, 0);

    given(sendResult.getRecordMetadata()).willReturn(recordMetadata);
    when(kafkaTemplate.send(anyString(), anyString(), any(FreebetOffer.class)))
        .thenReturn(responseFuture);
    doAnswer(
            invocationOnMock -> {
              ListenableFutureCallback listenableFutureCallback = invocationOnMock.getArgument(0);
              listenableFutureCallback.onSuccess(sendResult);
              assertEquals(sendResult.getRecordMetadata().offset(), offset);
              assertEquals(sendResult.getRecordMetadata().partition(), partition);
              return null;
            })
        .when(responseFuture)
        .addCallback(any(ListenableFutureCallback.class));
    abstractKafkaPublisher.publish(key, freebetOffer);
    verify(kafkaTemplate, times(1)).send(topic, key, freebetOffer);
  }

  @Test()
  void can_capture_failure_publishDataToKafka() {
    final String message = "some message";
    FreebetOffer freebetOffer = mock(FreebetOffer.class);
    ListenableFuture<SendResult<String, FreebetOffer>> responseFuture =
        mock(ListenableFuture.class);
    Throwable throwable = mock(Throwable.class);

    given(throwable.getMessage()).willReturn(message);
    when(kafkaTemplate.send(topic, key, freebetOffer)).thenReturn(responseFuture);
    doAnswer(
            invocationOnMock -> {
              ListenableFutureCallback listenableFutureCallback = invocationOnMock.getArgument(0);
              listenableFutureCallback.onFailure(throwable);
              return null;
            })
        .when(responseFuture)
        .addCallback(any(ListenableFutureCallback.class));
    abstractKafkaPublisher.publish(key, freebetOffer);
    verify(kafkaTemplate, times(1)).send(topic, key, freebetOffer);
  }
}
