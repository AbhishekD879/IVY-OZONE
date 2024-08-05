package com.ladbrokescoral.cashout.model.response;

import com.coral.bpp.api.model.bet.api.response.accountHistory.Paging;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.LottoBetResponse;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.PoolBet;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class InitialAccountHistoryBetResponse implements BetResponse {
  List<BetSummaryModel> bets;
  List<PoolBet> poolBets;
  List<LottoBetResponse> lottoBets;
  Paging paging;
  String token;
  String betCount;
}
