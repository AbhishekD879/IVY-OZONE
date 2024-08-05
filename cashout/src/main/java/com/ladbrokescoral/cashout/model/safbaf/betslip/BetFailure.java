package com.ladbrokescoral.cashout.model.safbaf.betslip;

import lombok.Data;

@Data
public class BetFailure {
  private String betNo;
  private String betFailureCode;
  private String betFailureDescription;
  private String betFailureReason;
  private FailureDetail failureDetail;
}
