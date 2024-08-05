package com.ladbrokescoral.cashout.model.response;

import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class UpdateBetResponse implements BetResponse {
  private Bet bet;
}
