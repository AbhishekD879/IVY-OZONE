package com.coral.oxygen.middleware.ms.quickbet.util;

import com.entain.oxygen.bettingapi.model.bet.api.common.YesNo;
import com.entain.oxygen.bettingapi.model.bet.api.response.Bet;
import java.text.DecimalFormat;
import org.apache.commons.lang3.StringUtils;

public class BettingApiBetUtils {
  private static final DecimalFormat df = new DecimalFormat("#.##");
  public static final String OPEN_BET_BIR_PROVIDER = "OpenBetBir";
  public static final String OPEN_BET_OVERASK_PROVIDER = "Overask";

  private BettingApiBetUtils() {}

  public static boolean isConfirmed(Bet bet) {
    return bet.getIsConfirmed() == null || YesNo.Y.equals(bet.getIsConfirmed());
  }

  public static boolean isBetOverask(Bet bet) {
    return !isConfirmed(bet) && YesNo.Y.equals(bet.getIsReferred());
  }

  public static boolean isBetInRun(Bet bet) {
    return !isConfirmed(bet)
        && OPEN_BET_BIR_PROVIDER.equalsIgnoreCase(bet.getProvider())
        && !StringUtils.isBlank(bet.getConfirmationExpectedAt());
  }

  public static boolean isCancelled(Bet bet) {
    return YesNo.Y.equals(bet.getIsCancelled());
  }
}
