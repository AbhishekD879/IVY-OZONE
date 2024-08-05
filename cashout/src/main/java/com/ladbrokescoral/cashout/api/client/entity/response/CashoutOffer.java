package com.ladbrokescoral.cashout.api.client.entity.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class CashoutOffer {
  private String cashoutOfferReqRef;
  private String status;
  private Double cashoutValue;
  private String message;
}
