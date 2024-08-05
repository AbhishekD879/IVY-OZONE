package com.coral.oxygen.middleware.ms.quickbet.util;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.LuckyDipBetPlacementRequest;
import org.apache.commons.lang3.StringUtils;

public class ValidatorUtils {

  private ValidatorUtils() {
    throw new IllegalStateException("Utility class");
  }

  public static void validateRequest(LuckyDipBetPlacementRequest request) {
    if (StringUtils.isBlank(request.getWinType())) {
      throw new IllegalArgumentException("WinType can't be empty");
    }
    if (StringUtils.isBlank(request.getStake())) {
      throw new IllegalArgumentException("Stake can't be empty");
    }
    if (StringUtils.isBlank(request.getMarketId())) {
      throw new IllegalArgumentException("MarketId can't be empty");
    }
    if (StringUtils.isBlank(request.getToken())) {
      throw new IllegalArgumentException("Token can't be empty");
    }
  }
}
