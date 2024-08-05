package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class StakeDto {
  private String stakePerLine;
  private String freebet;
  private String freebetOfferCategory;
  private String amount;
  private String maxAllowed;
  private String minAllowed;

  public StakeDto withStakePerLine(String stakePerLine) {
    this.stakePerLine = stakePerLine;
    return this;
  }

  public StakeDto withFreebetOfferCategory(String freebetOfferCategory) {
    this.freebetOfferCategory = freebetOfferCategory;
    return this;
  }

  public StakeDto withFreebet(String freebet) {
    this.freebet = freebet;
    return this;
  }

  public StakeDto withAmount(String amount) {
    this.amount = amount;
    return this;
  }

  public StakeDto withMaxAllowed(String maxAllowed) {
    this.maxAllowed = maxAllowed;
    return this;
  }

  public StakeDto withMinAllowed(String minAllowed) {
    this.minAllowed = minAllowed;
    return this;
  }
}
