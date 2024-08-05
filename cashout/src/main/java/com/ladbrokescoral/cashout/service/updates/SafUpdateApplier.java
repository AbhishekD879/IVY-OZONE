package com.ladbrokescoral.cashout.service.updates;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory;
import com.ladbrokescoral.cashout.model.safbaf.HasStatus;
import com.ladbrokescoral.cashout.service.SelectionData;
import com.ladbrokescoral.cashout.service.SelectionData.SelectionStatus;
import com.ladbrokescoral.cashout.service.updates.SelectionDataAwareUpdateProcessor.CashoutChange;
import com.ladbrokescoral.cashout.util.BetUtil;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.EnumSet;
import java.util.List;
import java.util.function.Function;

public interface SafUpdateApplier<T extends HasStatus> {

  default EnumSet<ChangeInfo> applyChange(SelectionData selectionData, T update) {
    EnumSet<ChangeInfo> changeSet = applySpecificChange(selectionData, update);
    boolean statusChanged = update.applyCurrentUpdateStatusIfItExists(selectionData);
    if (!statusChanged) {
      return changeSet;
    } else if (selectionData.getSelectionStatus() == SelectionStatus.ACTIVE) {
      changeSet.addAll(EnumSet.of(ChangeInfo.ACTIVATED));
    } else if (selectionData.getSelectionStatus() == SelectionStatus.SUSPENDED) {
      changeSet.addAll(EnumSet.of(ChangeInfo.SUSPENDED));
    }
    return changeSet;
  }

  default boolean needToCallServices(SelectionData selData, T update) {
    return true;
  }

  default EnumSet<ChangeInfo> applySpecificChange(SelectionData selectionData, T update) {
    return EnumSet.noneOf(ChangeInfo.class);
  }

  boolean couldChangeCashoutAvailability(UserRequestContextAccHistory context, T update);

  default boolean canSendCashoutUpdate(
      CashoutChange cashoutChange, BigInteger selectionId, BetSummaryModel bet) {
    return getCashoutUpdateConditions(cashoutChange, selectionId).stream()
        .anyMatch(c -> c.apply(bet));
  }

  default List<Function<BetSummaryModel, Boolean>> getCashoutUpdateConditions(
      CashoutChange cashoutChange, BigInteger selectionId) {
    EnumSet<ChangeInfo> changeSet = cashoutChange.getChangeSet();
    boolean isLpPriceChanged = changeSet.contains(ChangeInfo.LP_PRICE_CHANGED);
    boolean isSpPriceChanged = changeSet.contains(ChangeInfo.SP_PRICE_CHANGED);
    List<Function<BetSummaryModel, Boolean>> conditions = new ArrayList<>();
    conditions.add(bet -> (isSpPriceChanged && BetUtil.isBetOnSPPrice(bet, selectionId)));
    conditions.add(bet -> (isLpPriceChanged && BetUtil.isBetOnLPPrice(bet, selectionId)));
    return conditions;
  }

  enum ChangeInfo {
    LP_PRICE_CHANGED,
    SP_PRICE_CHANGED,
    ACTIVATED,
    SUSPENDED,
    CONFIRMED
  }
}
