package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet;

import com.entain.oxygen.bettingapi.model.bet.api.common.YesNo;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class BetDto {

  private Long id;
  private YesNo isReffered;
  private YesNo isConfirmed;
  private String cashoutValue;

  public BetDto id(Long id) {
    this.id = id;
    return this;
  }

  public BetDto isReffered(YesNo isReffered) {
    this.isReffered = isReffered;
    return this;
  }

  public BetDto isConfirmed(YesNo isConfirmed) {
    this.isConfirmed = isConfirmed;
    return this;
  }

  public BetDto withCashoutValue(String cashoutValue) {
    this.cashoutValue = cashoutValue;
    return this;
  }
}
