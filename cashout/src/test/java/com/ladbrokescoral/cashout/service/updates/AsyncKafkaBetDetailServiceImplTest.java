package com.ladbrokescoral.cashout.service.updates;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.coral.bpp.api.model.bet.api.request.GetBetDetailRequest;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.apache.kafka.common.TopicPartition;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.reactive.ReactiveKafkaProducerTemplate;
import reactor.core.publisher.Mono;
import reactor.kafka.sender.SenderResult;

@ExtendWith(MockitoExtension.class)
class AsyncKafkaBetDetailServiceImplTest {

  @Mock private ReactiveKafkaProducerTemplate<String, Object> reactiveKafkaProducerTemplate;
  @InjectMocks ReactiveAsyncKafkaBetDetailServiceImpl reactiveAsyncKafkaBetDetailServiceImpl;

  @SuppressWarnings({"rawtypes", "unchecked"})
  @Test
  void testAcceptBetDetailRequest() {
    BetDetailRequestCtx betDetailRequestCtx =
        BetDetailRequestCtx.builder()
            .request(GetBetDetailRequest.builder().token("123").build())
            .build();

    RecordMetadata meta = new RecordMetadata(new TopicPartition("test", 0), 0L, 0L, 0L, 0L, 0, 2);
    SenderResult result = mock(SenderResult.class);
    when(result.recordMetadata()).thenReturn(meta);
    Mockito.when(reactiveKafkaProducerTemplate.send(Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(Mono.just(result));
    reactiveAsyncKafkaBetDetailServiceImpl.acceptBetDetailRequest(betDetailRequestCtx);
    verify(reactiveKafkaProducerTemplate, times(1))
        .send(Mockito.any(), Mockito.any(), Mockito.any());
  }
}
