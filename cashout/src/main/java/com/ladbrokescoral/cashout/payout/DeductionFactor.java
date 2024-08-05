package com.ladbrokescoral.cashout.payout;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class DeductionFactor {
  private String numerator;
  private String denominator;
}
