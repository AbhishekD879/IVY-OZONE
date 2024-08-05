package com.ladbrokescoral.cashout.model.response;

import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class InitialBetResponse implements BetResponse {
  List<Bet> bets;
}
