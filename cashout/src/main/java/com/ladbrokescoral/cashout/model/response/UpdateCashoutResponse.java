package com.ladbrokescoral.cashout.model.response;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class UpdateCashoutResponse implements BetResponse {
  private CashoutData cashoutData;
  private ErrorCashout error;
}
