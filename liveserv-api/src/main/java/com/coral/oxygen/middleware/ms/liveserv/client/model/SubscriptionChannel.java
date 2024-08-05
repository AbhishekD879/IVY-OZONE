package com.coral.oxygen.middleware.ms.liveserv.client.model;

import com.coral.oxygen.middleware.ms.liveserv.model.ChannelType;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SubscriptionChannel {
  private ChannelType channelType;
  private Long channelId;
}
