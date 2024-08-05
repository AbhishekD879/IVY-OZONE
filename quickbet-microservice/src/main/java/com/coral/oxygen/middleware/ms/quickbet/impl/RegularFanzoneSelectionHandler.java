package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.*;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.USER_NOT_ALLOWED;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import java.util.Objects;
import java.util.regex.Pattern;
import org.apache.commons.lang3.StringUtils;
import org.jetbrains.annotations.Nullable;
import org.springframework.stereotype.Service;

@Service
public class RegularFanzoneSelectionHandler {
  private static final String FZ_MARKET = "MKTFLAG_FZ";
  private static final Pattern PATTERN = Pattern.compile("[,\\s]");
  private static final String ERROR_MSG = "User is not allowed to add this Fanzone selection";

  /**
   * validateFanzoneMarket this method will validate if the selection is FanPrice market or not and
   * verify user is allowed to add selection or not.
   *
   * @param request input request
   * @param market Event market from OB.
   */
  public void validateFanzoneMarket(RegularSelectionRequest request, Market market) {
    String fzMarketFlag = getFzMarketFlag(market);
    if (isaBoolean(fzMarketFlag)) {
      Outcome outcome = market.getOutcomes().get(0);
      String teamId =
          StringUtils.isNotBlank(outcome.getTeamExtIds())
              ? PATTERN.matcher(outcome.getTeamExtIds()).replaceAll("")
              : null;
      if (Objects.nonNull(teamId) && !(teamId.equals(request.getFanzoneTeamId()))) {
        throw new SiteServException(
            REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
            EVENT_NOT_FOUND.code(),
            USER_NOT_ALLOWED + ERROR_MSG);
      }
    }
  }

  /**
   * isaBoolean method will compare FanzoneMarket value and return true or false
   *
   * @param fzMarketFlag
   * @return boolean
   */
  private static boolean isaBoolean(String fzMarketFlag) {
    return StringUtils.isNotBlank(fzMarketFlag) && (FZ_MARKET.equals(fzMarketFlag));
  }

  /**
   * getFzMarketFlag method will check given market is fanPrice market or not from drillDownTagNames
   *
   * @param market
   * @return market flag
   */
  @Nullable
  private static String getFzMarketFlag(Market market) {
    return StringUtils.isNotBlank(market.getDrilldownTagNames())
        ? PATTERN.matcher(market.getDrilldownTagNames()).replaceAll("")
        : null;
  }

  /**
   * this validateFanPriceOutcome will be executed for logged out case and unsubscribed state while
   * adding fanzone selection
   *
   * @param market response from ss
   */
  public void validateFanPriceOutcome(Market market) {
    String fzMarketFlag = getFzMarketFlag(market);
    if (isaBoolean(fzMarketFlag)) {
      throw new SiteServException(
          REGULAR_OUTCOME_RESPONSE_ERROR_CODE,
          EVENT_NOT_FOUND.code(),
          USER_NOT_ALLOWED + ERROR_MSG);
    }
  }
}
