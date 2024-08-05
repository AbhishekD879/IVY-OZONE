package com.ladbrokescoral.cashout.model.safbaf;

import com.ladbrokescoral.cashout.service.SelectionData;
import java.math.BigInteger;
import java.util.Objects;
import java.util.Optional;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class Selection extends Entity implements HasStatus {
  private BigInteger selectionKey;
  private String selectionName;
  private String selectionStatus;
  private String resultCode;
  private String correctScoreHome;
  private String correctScoreAway;
  private Integer finalPosition;
  private Integer place;
  private Boolean isResultConfirmed;
  private Boolean isSettled;
  private Prices prices;
  private DeadHeat deadHeat;
  private Rule4 rule4;

  public Optional<String> getResultCode() {
    return Optional.ofNullable(this.resultCode);
  }

  public Optional<Boolean> getResultConfirmed() {
    return Optional.ofNullable(this.isResultConfirmed);
  }

  public Optional<Price> getLpPrice() {
    return findPriceByType("LP");
  }

  public Optional<Price> getSpPrice() {
    return findPriceByType("SP");
  }

  private Optional<Price> findPriceByType(String priceType) {
    return Optional.ofNullable(prices)
        .flatMap(
            pricesObj ->
                pricesObj.getPrice().stream()
                    .filter(price -> priceType.equalsIgnoreCase(price.getSelectionPriceType()))
                    .filter(
                        price ->
                            Objects.nonNull(price.getNumPrice())
                                && Objects.nonNull(price.getDenPrice()))
                    .findAny());
  }

  public boolean settledChanged() {
    return Objects.nonNull(this.isSettled);
  }

  public boolean resultCodeIsPresent() {
    return Objects.nonNull(this.resultCode);
  }

  public boolean isConfirmed() {
    return Objects.nonNull(this.isResultConfirmed);
  }

  public boolean priceUpdateExists() {
    return Objects.nonNull(this.prices);
  }

  public Optional<DeadHeat> getDeadHeat() {
    return Optional.ofNullable(deadHeat);
  }

  public Optional<Rule4> getRule4() {
    return Optional.ofNullable(rule4);
  }

  @Override
  public boolean changeStatus(SelectionData data, boolean newStatus) {
    return data.changeSelectionStatus(newStatus);
  }

  @Override
  public String getStatus() {
    return this.getSelectionStatus();
  }

  @Override
  public String reasonForUpdate() {
    if (resultCodeIsPresent()) {
      return "Resulted/Selection";
    } else if (statusChanged()) {
      return "StatusChanged/Selection/" + getSelectionStatus();
    } else if (settledChanged()) {
      return "Settled/Selection";
    } else if (priceUpdateExists()) {
      return "PriceChangedBanach";
    } else {
      return "Unknown/Selection";
    }
  }
}
