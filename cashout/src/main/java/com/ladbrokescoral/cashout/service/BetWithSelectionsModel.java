package com.ladbrokescoral.cashout.service;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import java.util.List;
import java.util.Optional;
import java.util.function.Supplier;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Singular;
import lombok.ToString;

/** Represents bet using list of {@link SelectionData} for each leg. */
@Data
@Builder
public class BetWithSelectionsModel {
  @EqualsAndHashCode.Exclude @Singular private List<SelectionDataLeg> legs;
  @ToString.Exclude private BetSummaryModel originalBet;
  private boolean isBanachBet;

  @RequiredArgsConstructor
  @ToString
  @EqualsAndHashCode
  public static class SelectionDataLeg {

    @Getter private final SelectionData selectionData;
    @ToString.Exclude private final Supplier<Optional<SelectionDataPrice>> priceFunc;

    public Optional<SelectionDataPrice> getLegPrice() {
      return priceFunc.get();
    }
  }
}
