package com.ladbrokescoral.cashout.model.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CashoutData {
  private String betId;
  private String cashoutValue;
  private String cashoutStatus;
  private Boolean shouldActivate;
}
