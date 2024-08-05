package com.ladbrokescoral.cashout.payout;

import java.util.List;
import lombok.Data;

@Data
public class PayoutContext {
  private List<PotentialReturns> voidedBetsPotentialReturns;
  private List<PayoutRequest> payoutRequests;
}
