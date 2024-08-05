package com.ladbrokescoral.oxygen.notification.entities.bet;

import lombok.Data;

@Data
public class FailureDetail {
  private String selectionKey;
  private String eventId;
  private String selectionName;
  private String eventName;
  private Double priceNum;
  private Double priceDen;
}
