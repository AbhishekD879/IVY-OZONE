package com.ladbrokescoral.cashout.api.client.entity.request;

import java.util.List;
import lombok.Builder;
import lombok.Data;
import lombok.Singular;

/*-
 * stakeAmount;  "1.0"
 * tokenValue;  "7.00"
 * betType;  "SGL, DBL, ACC6, TRX"
 * legType;  "E"
 */
@Data
@Builder
public class CashoutBet {
  private String stakeAmount;
  private String tokenValue;
  private String betType;
  private String legType;
  private String cashoutProfile;
  @Singular private List<CashoutLeg> legs;
}
