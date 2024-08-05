package com.ladbrokescoral.cashout.model.response;

import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@Builder
@EqualsAndHashCode(exclude = "timestamp")
public class UpdateDto {
  private CashoutData cashoutData;
  private Bet bet;
  private ErrorCashout error;
  private String timestamp;
}
