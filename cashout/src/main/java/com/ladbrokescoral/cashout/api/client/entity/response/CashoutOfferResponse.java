package com.ladbrokescoral.cashout.api.client.entity.response;

import java.util.List;
import lombok.Data;

@Data
public class CashoutOfferResponse {
  private String respStatus;
  private String timeStamp;
  private List<CashoutOffer> cashoutOffers;
  private String message;
}
