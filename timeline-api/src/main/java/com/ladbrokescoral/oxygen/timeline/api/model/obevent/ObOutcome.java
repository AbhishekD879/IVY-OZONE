package com.ladbrokescoral.oxygen.timeline.api.model.obevent;

import java.util.Collections;
import java.util.List;
import java.util.Optional;
import lombok.Data;

@Data
public class ObOutcome {
  private String id;
  private String marketId;
  private String name;
  private String outcomeMeaningMajorCode;
  private String outcomeMeaningMinorCode;
  private String outcomeMeaningScores;
  private Integer runnerNumber;
  private Boolean isResulted;
  private Integer displayOrder;
  private String outcomeStatusCode;
  private Boolean isActive = true;
  private Boolean isDisplayed = true;

  private List<ObPrice> prices;

  private String siteChannels;
  private String liveServChannels;
  private String liveServChildrenChannels;
  private String liveServLastMsgId;
  private String drilldownTagNames;
  private Boolean isAvailable;
  private Boolean isFinished;
  private String hasRestrictedSet;
  private Boolean isEnhancedOdds;
  private String cashoutAvail;
  private boolean hasPriceStream;

  public void applyOutcomeLiveUpdate(SelectionStatus selectionStatus) {
    this.isActive =
        selectionStatus.getActive() != null ? selectionStatus.getActive() : this.isActive;
    this.isResulted =
        selectionStatus.getSettled() != null ? selectionStatus.getSettled() : this.isResulted;
    this.isDisplayed =
        selectionStatus.getDisplayed() != null ? selectionStatus.getDisplayed() : this.isDisplayed;
    this.outcomeStatusCode = this.isActive ? "A" : "S";
    this.prices =
        applyPriceUpdate(selectionStatus)
            .map(obPrice -> Collections.singletonList(obPrice))
            .orElse(this.prices);
  }

  private Optional<ObPrice> applyPriceUpdate(SelectionStatus selectionStatus) {
    if (selectionStatus.getPriceDen() != null && selectionStatus.getPriceNum() != null) {
      return Optional.of(
          getFirstPrice()
              .map(
                  (ObPrice price) -> {
                    price.setPriceNum(selectionStatus.getPriceNum());
                    price.setPriceDen(selectionStatus.getPriceDen());
                    return price;
                  })
              .orElse(
                  ObPrice.builder()
                      .priceDen(selectionStatus.getPriceDen())
                      .priceNum(selectionStatus.getPriceNum())
                      .priceType("LP")
                      .isActive(true)
                      .build()));
    }
    return Optional.empty();
  }

  private Optional<ObPrice> getFirstPrice() {
    return prices != null && !prices.isEmpty() ? Optional.of(prices.get(0)) : Optional.empty();
  }
}
