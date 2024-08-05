package com.coral.oxygen.middleware.ms.liveserv.client.model;

import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SubscriptionRequest {
  private String topic;
  private List<SubscriptionChannel> channels;
}
