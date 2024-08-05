package com.ladbrokescoral.cashout.service.updates;

import com.ladbrokescoral.cashout.api.client.entity.request.CashoutOfferRequest;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest;
import com.ladbrokescoral.cashout.config.InternalKafkaTopics;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.kafka.core.reactive.ReactiveKafkaProducerTemplate;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Qualifier("cashoutOfferProxy")
public class ReactiveAsyncCashoutOfferServiceProxy implements AsyncCashoutOfferService {

  private final Logger log = LoggerFactory.getLogger(ReactiveAsyncCashoutOfferServiceProxy.class);

  private final ReactiveKafkaProducerTemplate<String, CashoutRequest>
      cashoutReqReactiveKafkaProducerTemplate;

  @Override
  public void acceptCashoutOfferRequest(CashoutRequest cashoutRequest) {
    String topicName = InternalKafkaTopics.CASHOUT_OFFER_REQUESTS.getTopicName();
    List<CashoutOfferRequest> cashoutRequestItems = cashoutRequest.getCashoutOfferRequests();

    CashoutOfferRequest cashoutRequestItem = cashoutRequestItems.get(0);
    cashoutReqReactiveKafkaProducerTemplate
        .send(topicName, cashoutRequestItem.getCashoutOfferReqRef(), cashoutRequest)
        .doOnSuccess(
            senderResult ->
                log.info(
                    "sent {} offset : {}", cashoutRequest, senderResult.recordMetadata().offset()))
        .subscribe();
  }
}
