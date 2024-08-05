package com.ladbrokescoral.cashout.payout;

import java.util.List;

public interface PayoutService {

  List<PotentialReturns> getPotentialReturns(List<PayoutRequest> payoutRequests);
}
