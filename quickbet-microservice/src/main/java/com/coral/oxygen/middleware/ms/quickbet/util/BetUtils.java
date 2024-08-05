package com.coral.oxygen.middleware.ms.quickbet.util;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.FreeBetRequest;
import java.math.BigDecimal;
import java.text.DecimalFormat;
import org.apache.commons.lang3.StringUtils;
import org.springframework.util.Assert;

public class BetUtils {
  private static final DecimalFormat df = new DecimalFormat("#.##");
  public static final String OPEN_BET_BIR_PROVIDER = "OpenBetBir";
  public static final String OPEN_BET_OVERASK_PROVIDER = "Overask";

  private BetUtils() {}

  public static String calculateTotalStakeWithFreeBet(String userStake, FreeBetRequest freebet) {
    Assert.notNull(freebet.getStake(), "Freebet stake cannot be null");
    BigDecimal userStakeAsNumber = new BigDecimal(StringUtils.isBlank(userStake) ? "0" : userStake);
    BigDecimal totalStakeAsNumber = userStakeAsNumber.add(new BigDecimal(freebet.getStake()));
    return df.format(totalStakeAsNumber);
  }
}
