package com.ladbrokescoral.cashout.api.client.entity.request;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class CashoutOfferRequest {
  private String cashoutOfferReqRef;
  private CashoutBet bet;
}
