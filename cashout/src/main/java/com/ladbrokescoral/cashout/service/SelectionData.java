package com.ladbrokescoral.cashout.service;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.ConfirmingResult;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Part;
import com.ladbrokescoral.cashout.model.ResultCode;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.function.Consumer;
import lombok.AccessLevel;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

/**
 * Represents event/market/selection hierarchy. Holds status of event, market and status separately.
 * Contains a set of legs where this selection is used.
 */
@ToString
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class SelectionData {
  final Lock priceLock = new ReentrantLock();

  @Getter private List<BetSummaryModel> bets = new ArrayList<>();
  @ToString.Exclude @Getter private List<Part> parts = new ArrayList<>();

  @EqualsAndHashCode.Include @Getter private BigInteger eventId;
  @EqualsAndHashCode.Include @Getter private BigInteger marketId;
  @EqualsAndHashCode.Include @Getter private BigInteger selectionId;

  @Getter
  @Setter(value = AccessLevel.PRIVATE)
  private volatile Boolean eventActive;

  @Getter
  @Setter(value = AccessLevel.PRIVATE)
  private volatile Boolean marketActive;

  @Getter
  @Setter(value = AccessLevel.PRIVATE)
  private volatile Boolean selectionActive;

  private volatile SelectionDataPrice lpPrice;
  private volatile SelectionDataPrice spPrice;
  @Getter @Setter private boolean confirmed;
  @Getter @Setter private boolean handicapMarket;

  public SelectionData(BigInteger eventId, BigInteger marketId, BigInteger selectionId) {
    this.eventId = eventId;
    this.marketId = marketId;
    this.selectionId = selectionId;
  }

  public SelectionData(
      List<BetSummaryModel> bets,
      List<Part> parts,
      BigInteger eventId,
      BigInteger marketId,
      BigInteger selectionId) {
    this.bets = bets;
    this.parts = parts;
    this.eventId = eventId;
    this.marketId = marketId;
    this.selectionId = selectionId;
  }

  public SelectionStatus getSelectionStatus() {
    if (Boolean.FALSE.equals(selectionActive)
        || Boolean.FALSE.equals(marketActive)
        || Boolean.FALSE.equals(eventActive)) {
      return SelectionStatus.SUSPENDED;
    } else if (selectionActive == null || marketActive == null || eventActive == null) {
      return SelectionStatus.UNKNOWN;
    } else {
      return SelectionStatus.ACTIVE;
    }
  }

  public Optional<SelectionDataPrice> getLpPrice() {
    return Optional.ofNullable(lpPrice);
  }

  public Optional<SelectionDataPrice> getSpPrice() {
    return Optional.ofNullable(spPrice);
  }

  /** Changes LP price. Returns true if changed, false otherwise */
  public boolean changeLpPrice(int num, int den) {
    SelectionDataPrice newPrice = new SelectionDataPrice(num, den);
    priceLock.lock();
    try {
      if (!newPrice.equals(this.lpPrice)) {
        this.lpPrice = new SelectionDataPrice(num, den);
        updatePricesInBets(AccountHistoryPriceType.L, newPrice);
        return true;
      }
      return false;
    } finally {
      priceLock.unlock();
    }
  }

  /** Changes SP price. Returns true if changed, false otherwise */
  public boolean changeSpPrice(int num, int den) {
    SelectionDataPrice newPrice = new SelectionDataPrice(num, den);
    priceLock.lock();
    try {
      if (!newPrice.equals(spPrice)) {
        this.spPrice = newPrice;
        updatePricesInBets(AccountHistoryPriceType.S, newPrice);
        return true;
      }

      return false;
    } finally {
      priceLock.unlock();
    }
  }

  private void updatePricesInBets(AccountHistoryPriceType priceType, SelectionDataPrice newPrice) {
    this.parts.stream()
        .flatMap(p -> p.getPrice().stream())
        .filter(p -> priceType.name().equalsIgnoreCase(p.getPriceType().getCode()))
        .forEach(
            p -> {
              if (priceType == AccountHistoryPriceType.S) {
                p.setPriceStartingNum(String.valueOf(newPrice.getNum()));
                p.setPriceStartingDen(String.valueOf(newPrice.getDen()));
              } else if (priceType == AccountHistoryPriceType.L) {
                p.setCurrentPriceNum(String.valueOf(newPrice.getNum()));
                p.setCurrentPriceDen(String.valueOf(newPrice.getDen()));
              }
            });
  }

  public void updateResultCode(ResultCode resultCode, Integer places) {
    if (resultCode != ResultCode.UNKNOWN) {
      for (Part part : parts) {
        ConfirmingResult result = part.getOutcome().get(0).getResult();
        if (resultCode == ResultCode.PLACE && places != null) {
          result.setPlaces(String.valueOf(places));
        }
        result.setValue(resultCode.getAccHistoryResultCode());
        if (resultCode == ResultCode.UNSET) {
          result.setPlaces("");
        }
      }
    }
  }

  public boolean changeSelectionStatus(boolean selectionActive) {
    return changeStatus(this::setSelectionActive, selectionActive);
  }

  public boolean changeMarketStatus(boolean marketActive) {
    return changeStatus(this::setMarketActive, marketActive);
  }

  public boolean changeEventStatus(boolean eventActive) {
    return changeStatus(this::setEventActive, eventActive);
  }

  private boolean changeStatus(Consumer<Boolean> statusChanger, boolean status) {
    SelectionStatus oldStatus = this.getSelectionStatus();
    statusChanger.accept(status);
    return oldStatus != this.getSelectionStatus();
  }

  public boolean hasUnknownStatusOrLpPrice() {
    return getEventActive() == null
        || getMarketActive() == null
        || getSelectionActive() == null
        || !getLpPrice().isPresent();
  }

  public Boolean updateConfirmed(Boolean confirmed) {
    this.confirmed = confirmed;
    return confirmed;
  }

  public boolean belongToHandicapActiveMarket() {
    return getSelectionStatus().equals(SelectionStatus.ACTIVE) && isHandicapMarket();
  }

  public enum SelectionStatus {
    ACTIVE,
    SUSPENDED,
    UNKNOWN
  }

  public enum AccountHistoryPriceType {
    S,
    L
  }
}
