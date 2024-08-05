package com.ladbrokescoral.cashout.payout;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetType;

public class PayoutUtil {

  private PayoutUtil() {}

  public static String getBetType(BetType betType) {
    String bet = betType.getCode();
    if (bet.startsWith("AC") || (bet.startsWith("P") && !bet.equals("PAT"))) {
      bet = "ACCA";
    }
    return bet;
  }
}
