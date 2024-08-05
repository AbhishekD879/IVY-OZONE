package com.ladbrokescoral.cashout.config;

import static org.mockito.Mockito.when;

import com.coral.bpp.api.model.bet.api.request.GetBetDetailRequest;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutBet;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutOfferRequest;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest;
import com.ladbrokescoral.cashout.model.response.CashoutData;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import com.ladbrokescoral.cashout.service.UserFluxBetUpdatesContext;
import com.ladbrokescoral.cashout.service.UserUpdatesContext;
import com.ladbrokescoral.cashout.service.updates.AsyncBetDetailService;
import com.ladbrokescoral.cashout.service.updates.AsyncCashoutOfferService;
import com.ladbrokescoral.cashout.service.updates.BetDetailRequestCtx;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.header.Header;
import org.apache.kafka.common.header.Headers;
import org.apache.kafka.common.header.internals.RecordHeaders;
import org.apache.kafka.common.record.TimestampType;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.kafka.core.reactive.ReactiveKafkaConsumerTemplate;
import org.springframework.test.util.ReflectionTestUtils;
import reactor.core.publisher.Flux;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class ReactiveInternalKafkaMessageListenerTest {

  @InjectMocks ReactiveInternalKafkaMessageListener InternalKafkaMessageListener;

  @Mock private AsyncBetDetailService asyncBetDetailService;
  @Mock private AsyncCashoutOfferService asyncCashoutService;
  @Mock private UserUpdatesContext userUpdatesContext;
  @Mock private UserFluxBetUpdatesContext userFluxBetUpdatesContext;
  @Mock private ReactiveKafkaConsumerTemplate<String, Object> reactiveKafkaConsumerTemplate;

  @Test
  void triggerBetDetailsRequestTest() throws Exception {
    ReflectionTestUtils.setField(InternalKafkaMessageListener, "overflowStrategy", "DROP_OLDEST");
    List<Header> headers = new ArrayList<>();
    Headers header = new RecordHeaders(headers);
    CashoutData cashoutData = CashoutData.builder().betId("12345").cashoutStatus("SUCCESS").build();
    UpdateDto updateDto1 = UpdateDto.builder().cashoutData(cashoutData).timestamp("now").build();
    ConsumerRecord<String, Object> record3 =
        new ConsumerRecord<>(
            "bet-updates",
            0,
            0,
            123,
            TimestampType.NO_TIMESTAMP_TYPE,
            123L,
            1,
            1,
            "bet-updates",
            updateDto1,
            header);
    when(reactiveKafkaConsumerTemplate.receiveAutoAck()).thenReturn(Flux.just(record3));
    InternalKafkaMessageListener.run();
    Mockito.verify(userFluxBetUpdatesContext).sendBetUpdate(Mockito.any(), Mockito.any());
  }

  @Test
  void testBetDetailsRequest() throws Exception {
    ReflectionTestUtils.setField(InternalKafkaMessageListener, "overflowStrategy", "DROP_OLDEST");
    List<Header> headers = new ArrayList<>();
    Headers header = new RecordHeaders(headers);
    ConsumerRecord<String, BetDetailRequestCtx> record =
        new ConsumerRecord<>(
            "bet-detail-requests",
            0,
            0,
            123,
            TimestampType.NO_TIMESTAMP_TYPE,
            123L,
            1,
            1,
            "bet-detail-requests",
            createGetBetDetailRequest("12345"),
            header);
    InternalKafkaMessageListener.betDetailsRequest(record);
    Mockito.verify(asyncBetDetailService).acceptBetDetailRequest(Mockito.any());
  }

  @Test
  void testCashoutRequest() throws Exception {
    ReflectionTestUtils.setField(InternalKafkaMessageListener, "overflowStrategy", "DROP_OLDEST");
    List<Header> headers = new ArrayList<>();
    Headers header = new RecordHeaders(headers);
    ConsumerRecord<String, CashoutRequest> record =
        new ConsumerRecord<>(
            "cashout-offer-requests",
            0,
            0,
            123,
            TimestampType.NO_TIMESTAMP_TYPE,
            123L,
            1,
            1,
            "cashout-offer-requests",
            createCashoutRequest("12345"),
            header);
    InternalKafkaMessageListener.cashoutRequest(record);
    Mockito.verify(asyncCashoutService).acceptCashoutOfferRequest(Mockito.any());
  }

  @Test
  void testBetUpdate() throws Exception {
    ReflectionTestUtils.setField(InternalKafkaMessageListener, "overflowStrategy", "DROP_OLDEST");
    List<Header> headers = new ArrayList<>();
    Headers header = new RecordHeaders(headers);
    UpdateDto updateDto = UpdateDto.builder().timestamp("now").build();
    ConsumerRecord<String, UpdateDto> record =
        new ConsumerRecord<>(
            "bet-updates",
            0,
            0,
            123,
            TimestampType.NO_TIMESTAMP_TYPE,
            123L,
            1,
            1,
            "bet-updates",
            updateDto,
            header);
    InternalKafkaMessageListener.betUpdate(record);
    Mockito.verify(userFluxBetUpdatesContext).sendBetUpdate(Mockito.any(), Mockito.any());
  }

  @Test
  void testBetUpdateError() throws Exception {
    ReflectionTestUtils.setField(InternalKafkaMessageListener, "overflowStrategy", "DROP_OLDEST");
    List<Header> headers = new ArrayList<>();
    Headers header = new RecordHeaders(headers);
    ConsumerRecord<String, Throwable> record =
        new ConsumerRecord<>(
            "bet-updates-errors",
            0,
            0,
            123,
            TimestampType.NO_TIMESTAMP_TYPE,
            123L,
            1,
            1,
            "bet-updates-errors",
            new Throwable("error"),
            header);
    InternalKafkaMessageListener.betUpdateError(record);
    Mockito.verify(userUpdatesContext).sendBetUpdateError(Mockito.any(), Mockito.any());
  }

  private CashoutRequest createCashoutRequest(String betId) {
    return CashoutRequest.builder()
        .cashoutOfferRequests(
            Collections.singletonList(
                CashoutOfferRequest.builder()
                    .cashoutOfferReqRef(betId)
                    .bet(CashoutBet.builder().betType("SGL").build())
                    .build()))
        .build();
  }

  private BetDetailRequestCtx createGetBetDetailRequest(String betId) {
    return BetDetailRequestCtx.builder()
        .userId("abc")
        .timeToTokenExpirationLeft(null)
        .request(
            GetBetDetailRequest.builder()
                .token("abc")
                .betIds(Collections.singletonList(betId))
                .build())
        .build();
  }
}
