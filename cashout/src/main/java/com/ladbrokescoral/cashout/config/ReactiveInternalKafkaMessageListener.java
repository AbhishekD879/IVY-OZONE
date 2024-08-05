package com.ladbrokescoral.cashout.config;

import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest;
import com.ladbrokescoral.cashout.model.Code;
import com.ladbrokescoral.cashout.model.response.ErrorBetResponse;
import com.ladbrokescoral.cashout.model.response.UpdateBetResponse;
import com.ladbrokescoral.cashout.model.response.UpdateCashoutResponse;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import com.ladbrokescoral.cashout.service.UserFluxBetUpdatesContext;
import com.ladbrokescoral.cashout.service.UserUpdatesContext;
import com.ladbrokescoral.cashout.service.updates.AsyncBetDetailService;
import com.ladbrokescoral.cashout.service.updates.AsyncCashoutOfferService;
import com.ladbrokescoral.cashout.service.updates.BetDetailRequestCtx;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.kafka.core.reactive.ReactiveKafkaConsumerTemplate;
import org.springframework.stereotype.Service;
import reactor.core.publisher.BufferOverflowStrategy;
import reactor.core.publisher.Flux;

@Service
public class ReactiveInternalKafkaMessageListener implements CommandLineRunner {

  @Value("${cashout-offer-requests.max.poll.records:100}")
  private int maxPollRecords;

  @Value("${cashout-offer.requests.overflow-strategy}")
  private String overflowStrategy;

  private AsyncBetDetailService asyncBetDetailService;
  private AsyncCashoutOfferService asyncCashoutService;
  private UserUpdatesContext userUpdatesContext;
  private UserFluxBetUpdatesContext userFluxBetUpdatesContext;
  private ReactiveKafkaConsumerTemplate<String, BetDetailRequestCtx> reactiveKafkaConsumerTemplate;
  private ReactiveKafkaConsumerTemplate<String, CashoutRequest>
      betDetailreactiveKafkaConsumerTemplate;
  private ReactiveKafkaConsumerTemplate<String, UpdateDto> betUpdatesReactiveKafkaConsumerTemplate;
  private ReactiveKafkaConsumerTemplate<String, Throwable>
      betUpdatesErrorReactiveKafkaConsumerTemplate;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Autowired
  public ReactiveInternalKafkaMessageListener(
      AsyncBetDetailService asyncBetDetailService,
      AsyncCashoutOfferService asyncCashoutService,
      UserUpdatesContext userUpdatesContext,
      UserFluxBetUpdatesContext userFluxBetUpdatesContext,
      ReactiveKafkaConsumerTemplate<String, BetDetailRequestCtx> reactiveKafkaConsumerTemplate,
      ReactiveKafkaConsumerTemplate<String, CashoutRequest> betDetailreactiveKafkaConsumerTemplate,
      ReactiveKafkaConsumerTemplate<String, UpdateDto> betUpdatesReactiveKafkaConsumerTemplate,
      ReactiveKafkaConsumerTemplate<String, Throwable>
          betUpdatesErrorReactiveKafkaConsumerTemplate) {
    this.asyncBetDetailService = asyncBetDetailService;
    this.asyncCashoutService = asyncCashoutService;
    this.userUpdatesContext = userUpdatesContext;
    this.userFluxBetUpdatesContext = userFluxBetUpdatesContext;
    this.reactiveKafkaConsumerTemplate = reactiveKafkaConsumerTemplate;
    this.betDetailreactiveKafkaConsumerTemplate = betDetailreactiveKafkaConsumerTemplate;
    this.betUpdatesReactiveKafkaConsumerTemplate = betUpdatesReactiveKafkaConsumerTemplate;
    this.betUpdatesErrorReactiveKafkaConsumerTemplate =
        betUpdatesErrorReactiveKafkaConsumerTemplate;
  }

  @Override
  public void run(String... args) throws Exception {
    consumeBetDetailsRequest().subscribe();
    consumeCashoutRequest().subscribe();
    consumeBetUpdate().subscribe();
    consumeBetUpdateError().subscribe();
  }

  public Flux<ConsumerRecord<String, BetDetailRequestCtx>> consumeBetDetailsRequest() {
    return reactiveKafkaConsumerTemplate
        .receiveAutoAck()
        .onBackpressureBuffer(maxPollRecords, BufferOverflowStrategy.valueOf(overflowStrategy))
        .doOnNext(this::betDetailsRequest);
  }

  public void betDetailsRequest(ConsumerRecord<String, BetDetailRequestCtx> betDetailRequestCtx) {
    ASYNC_LOGGER.info("BetDetailRequestCtx::{}", betDetailRequestCtx.value());
    asyncBetDetailService.acceptBetDetailRequest(betDetailRequestCtx.value());
  }

  public Flux<ConsumerRecord<String, CashoutRequest>> consumeCashoutRequest() {
    return betDetailreactiveKafkaConsumerTemplate
        .receiveAutoAck()
        .onBackpressureBuffer(maxPollRecords, BufferOverflowStrategy.valueOf(overflowStrategy))
        .doOnNext(this::cashoutRequest);
  }

  public void cashoutRequest(ConsumerRecord<String, CashoutRequest> cashoutrequest) {
    ASYNC_LOGGER.info("cashoutrequest::{}", cashoutrequest.value());
    asyncCashoutService.acceptCashoutOfferRequest(cashoutrequest.value());
  }

  public Flux<ConsumerRecord<String, UpdateDto>> consumeBetUpdate() {
    return betUpdatesReactiveKafkaConsumerTemplate.receiveAutoAck().doOnNext(this::betUpdate);
  }

  public void betUpdate(ConsumerRecord<String, UpdateDto> betUpdateRecord) {
    String recordId = betUpdateRecord.key();
    if (betUpdateRecord.value().getCashoutData() != null) {
      userUpdatesContext.sendCashoutUpdate(
          recordId, new UpdateCashoutResponse(betUpdateRecord.value().getCashoutData(), null));
    } else {
      userUpdatesContext.sendBetUpdate(
          recordId, new UpdateBetResponse(betUpdateRecord.value().getBet()));
    }
    userFluxBetUpdatesContext.sendBetUpdate(recordId, betUpdateRecord.value());
  }

  public Flux<ConsumerRecord<String, Throwable>> consumeBetUpdateError() {
    return betUpdatesErrorReactiveKafkaConsumerTemplate
        .receiveAutoAck()
        .doOnNext(this::betUpdateError);
  }

  public void betUpdateError(ConsumerRecord<String, Throwable> betUpdateExceptionError) {
    userUpdatesContext.sendBetUpdateError(
        betUpdateExceptionError.key(),
        ErrorBetResponse.create(Code.fromException(betUpdateExceptionError.value())));

    userFluxBetUpdatesContext.sendException(
        betUpdateExceptionError.key(), betUpdateExceptionError.value());
  }
}
