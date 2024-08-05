package com.ladbrokescoral.cashout.service;

import com.ladbrokescoral.cashout.service.BetWithSelectionsModel.SelectionDataLeg;
import com.ladbrokescoral.cashout.service.SelectionData.SelectionStatus;
import java.util.List;
import org.apache.commons.collections4.CollectionUtils;

public enum CashoutAvailability {
  YES,
  NO,
  /** All legs confirmed, hence no cashout available */
  NO_CONFIRMED,
  /** When selection is suspended but has uncompetitive price (<=1/100) */
  UNKNOWN_UNCOMPETITIVE,
  /**
   * Represents a state when we don't know if cashout is available and need to request that info
   * from OpenBet
   */
  UNKNOWN;

  public static CashoutAvailability calculateCashoutAvailability(
      BetWithSelectionsModel bet, List<String> twoUpMarkets) {
    if (bet.isBanachBet()) {
      return UNKNOWN;
    }

    boolean allLegsConfirmed =
        bet.getLegs().stream().allMatch(l -> l.getSelectionData().isConfirmed());

    if (allLegsConfirmed) {
      return NO_CONFIRMED;
    }

    for (SelectionDataLeg selectionLeg : bet.getLegs()) {
      SelectionData selectionData = selectionLeg.getSelectionData();
      SelectionStatus selectionStatus = selectionData.getSelectionStatus();
      boolean isCompetitivePrice =
          selectionLeg.getLegPrice().map(SelectionDataPrice::isCompetitive).orElse(false);
      boolean confirmed = selectionData.isConfirmed();

      if (confirmed && selectionData.isHandicapMarket()) {
        return UNKNOWN;
      } else if (isUnknownUncompetitive(
          twoUpMarkets, selectionData, selectionStatus, isCompetitivePrice, confirmed)) {
        return UNKNOWN_UNCOMPETITIVE;
      } else if (isCashOutAvalibilityNo(selectionStatus, isCompetitivePrice, confirmed)) {
        return NO;
      } else if (selectionStatus != SelectionStatus.ACTIVE && !confirmed) {
        return UNKNOWN;
      }
    }
    return YES;
  }

  private static boolean isCashOutAvalibilityNo(
      SelectionStatus selectionStatus, boolean isCompetitivePrice, boolean confirmed) {
    return selectionStatus == SelectionStatus.SUSPENDED && isCompetitivePrice && !confirmed;
  }

  private static boolean isUnknownUncompetitive(
      List<String> twoUpMarkets,
      SelectionData selectionData,
      SelectionStatus selectionStatus,
      boolean isCompetitivePrice,
      boolean confirmed) {
    return selectionStatus != SelectionStatus.ACTIVE
        && (!isCompetitivePrice || isTwoUpMarket(twoUpMarkets, selectionData))
        && !confirmed;
  }

  private static boolean isTwoUpMarket(List<String> twoUpMarkets, SelectionData selectionData) {
    return CollectionUtils.isNotEmpty(twoUpMarkets)
        && selectionData.getParts().stream()
            .anyMatch(
                outCome ->
                    outCome.getOutcome().stream()
                        .anyMatch(
                            market ->
                                twoUpMarkets.stream()
                                    .anyMatch(
                                        marketName ->
                                            marketName.equalsIgnoreCase(
                                                market.getMarket().getName()))));
  }
}
