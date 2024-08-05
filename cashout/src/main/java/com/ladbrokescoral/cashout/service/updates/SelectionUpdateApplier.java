package com.ladbrokescoral.cashout.service.updates;

import com.ladbrokescoral.cashout.model.ResultCode;
import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory;
import com.ladbrokescoral.cashout.model.safbaf.Price;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import com.ladbrokescoral.cashout.service.SelectionData;
import java.math.BigInteger;
import java.util.EnumSet;
import java.util.Objects;
import java.util.function.BiFunction;
import org.springframework.stereotype.Component;

@Component
public class SelectionUpdateApplier implements SafUpdateApplier<Selection> {

  @Override
  public EnumSet<ChangeInfo> applySpecificChange(SelectionData selectionData, Selection update) {
    boolean isSpPriceChanged =
        update
            .getSpPrice()
            .map(p -> applyPriceChange(selectionData::changeSpPrice, p))
            .orElse(false);

    boolean isLpPriceChanged =
        update
            .getLpPrice()
            .map(p -> applyPriceChange(selectionData::changeLpPrice, p))
            .orElse(false);

    // save win/lost/void to memory model
    update
        .getResultCode()
        .map(ResultCode::fromSAFResultCode)
        .ifPresent(code -> selectionData.updateResultCode(code, update.getPlace()));

    boolean confirmed =
        update.getResultConfirmed().map(selectionData::updateConfirmed).orElse(false);

    //    EnumSet
    EnumSet<ChangeInfo> changeSet =
        EnumSet.of(ChangeInfo.LP_PRICE_CHANGED, ChangeInfo.SP_PRICE_CHANGED, ChangeInfo.CONFIRMED);

    if (!isLpPriceChanged) {
      changeSet.remove(ChangeInfo.LP_PRICE_CHANGED);
    }

    if (!isSpPriceChanged) {
      changeSet.remove(ChangeInfo.SP_PRICE_CHANGED);
    }

    if (!confirmed) {
      changeSet.remove(ChangeInfo.CONFIRMED);
    }

    return changeSet;
  }

  @Override
  public boolean couldChangeCashoutAvailability(
      UserRequestContextAccHistory context, Selection update) {
    return ((isHandicapMarket(context, update.getSelectionKey()) && update.isConfirmed())
        || update.statusChanged());
  }

  private boolean applyPriceChange(
      BiFunction<Integer, Integer, Boolean> priceChanger, Price selectionUpdatePrice) {
    return priceChanger.apply(
        selectionUpdatePrice.getNumPrice(), selectionUpdatePrice.getDenPrice());
  }

  @Override
  public boolean needToCallServices(SelectionData selData, Selection update) {
    return !(update.getResultCode().isPresent() && Objects.isNull(update.getStatus()));
  }

  private Boolean isHandicapMarket(UserRequestContextAccHistory context, BigInteger selectionId) {
    return context
        .getIndexedData()
        .getSelectionDataBySelectionId(selectionId)
        .map(SelectionData::belongToHandicapActiveMarket)
        .orElse(false);
  }
}
