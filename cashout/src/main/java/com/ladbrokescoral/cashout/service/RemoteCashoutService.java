package com.ladbrokescoral.cashout.service;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.ladbrokescoral.cashout.model.response.CashoutData;
import java.util.List;
import reactor.core.publisher.Flux;

public interface RemoteCashoutService {

  Flux<CashoutData> getCashout(List<BetSummaryModel> bets);
}
