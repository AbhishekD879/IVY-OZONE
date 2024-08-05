package com.ladbrokescoral.cashout.service.updates;

import com.ladbrokescoral.cashout.config.InternalKafkaTopics;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.kafka.core.reactive.ReactiveKafkaProducerTemplate;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Qualifier("kafka-bet-details")
public class ReactiveAsyncKafkaBetDetailServiceImpl implements AsyncBetDetailService {

  private final Logger log = LoggerFactory.getLogger(ReactiveAsyncKafkaBetDetailServiceImpl.class);

  private final ReactiveKafkaProducerTemplate<String, BetDetailRequestCtx>
      betDetailReactiveKafkaProducerTemplate;

  @Override
  public void acceptBetDetailRequest(BetDetailRequestCtx requestCtx) {
    betDetailReactiveKafkaProducerTemplate
        .send(
            InternalKafkaTopics.BET_DETAIL_REQUESTS.getTopicName(),
            requestCtx.getRequest().getToken(),
            requestCtx)
        .doOnSuccess(
            senderResult ->
                log.info("sent {} offset : {}", requestCtx, senderResult.recordMetadata().offset()))
        .subscribe();
  }
}
