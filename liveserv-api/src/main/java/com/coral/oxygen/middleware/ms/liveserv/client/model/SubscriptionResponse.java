package com.coral.oxygen.middleware.ms.liveserv.client.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SubscriptionResponse {

  private SubscriptionStatus status;
  private String message;

  public static SubscriptionResponse failed(String message) {
    return new SubscriptionResponse(SubscriptionStatus.FAILURE, message);
  }
}
