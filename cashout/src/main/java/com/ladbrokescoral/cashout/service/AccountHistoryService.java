package com.ladbrokescoral.cashout.service;

import com.coral.bpp.api.model.bet.api.request.AccountHistoryRequest;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.ladbrokescoral.cashout.model.response.InitialAccountHistoryBetResponse;
import java.util.List;
import reactor.core.publisher.Mono;

public interface AccountHistoryService {

  Mono<InitialAccountHistoryBetResponse> accountHistoryInitBets(
      AccountHistoryRequest accountHistoryRequest);

  Mono<List<BetSummaryModel>> getDetailedAccountHistoryWithOpenBetsOnly(String bppToken);
}
