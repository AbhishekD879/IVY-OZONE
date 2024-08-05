package com.ladbrokescoral.cashout.service.updates;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.cashout.api.client.entity.request.CashoutOfferRequest;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest;
import java.util.Collections;
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
class AsyncCashoutOfferServiceProxyTest {

  @Mock private ReactiveKafkaProducerTemplate<String, Object> reactiveKafkaProducerTemplate;
  @InjectMocks ReactiveAsyncCashoutOfferServiceProxy reactiveAsyncCashoutOfferServiceProxy;

  @SuppressWarnings({"rawtypes", "unchecked"})
  @Test
  void testAcceptCashoutOfferRequest() {
    CashoutRequest cashoutRequest =
        CashoutRequest.builder()
            .cashoutOfferRequests(
                Collections.singletonList(
                    CashoutOfferRequest.builder().cashoutOfferReqRef("123").build()))
            .build();

    RecordMetadata meta = new RecordMetadata(new TopicPartition("test", 0), 0L, 0L, 0L, 0L, 0, 2);
    SenderResult result = mock(SenderResult.class);
    when(result.recordMetadata()).thenReturn(meta);
    Mockito.when(reactiveKafkaProducerTemplate.send(Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(Mono.just(result));
    reactiveAsyncCashoutOfferServiceProxy.acceptCashoutOfferRequest(cashoutRequest);
    verify(reactiveKafkaProducerTemplate, times(1))
        .send(Mockito.any(), Mockito.any(), Mockito.any());
  }
}
