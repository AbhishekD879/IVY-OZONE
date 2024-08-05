package com.ladbrokescoral.oxygen.notification.entities.bet;

import lombok.Data;

@Data
public class BetFailure {
  private String betNo;
  private String betFailureCode;
  private String betFailureDescription;
  private String betFailureReason;
  private FailureDetail failureDetail;
}
