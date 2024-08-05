package com.ladbrokescoral.cashout.model.response;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class InitialAccountHistoryBetResponseModel implements BetResponse {
  List<BetSummaryModel> bets;
}
