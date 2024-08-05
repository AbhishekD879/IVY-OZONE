package com.ladbrokescoral.cashout.service;

import com.coral.bpp.api.model.bet.api.request.AccountHistoryRequest;
import com.coral.bpp.api.model.bet.api.request.GetBetDetailRequest;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet;
import com.ladbrokescoral.cashout.model.response.InitialAccountHistoryBetResponse;
import java.util.List;
import reactor.core.publisher.Mono;

public interface BppService {
  Mono<List<Bet>> getBetDetail(GetBetDetailRequest getBetDetailRequest);

  Mono<InitialAccountHistoryBetResponse> accountHistory(
      AccountHistoryRequest accountHistoryRequest);

  Mono<List<BetSummaryModel>> accountHistoryOpenBets(AccountHistoryRequest accountHistoryRequest);
}
