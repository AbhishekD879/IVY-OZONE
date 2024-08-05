package com.ladbrokescoral.cashout.service.updates;

import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest;

public interface AsyncCashoutOfferService {

  void acceptCashoutOfferRequest(CashoutRequest cashoutRequest);
}
