package com.ladbrokescoral.cashout.api.client;

import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest;
import com.ladbrokescoral.cashout.api.client.entity.response.CashoutOffer;
import reactor.core.publisher.Flux;

public interface RemoteCashoutApi {

  Flux<CashoutOffer> getCashoutOffers(CashoutRequest request);
}
