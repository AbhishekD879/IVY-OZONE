package com.coral.oxygen.middleware.ms.liveserv.newclient;

import com.coral.oxygen.middleware.ms.liveserv.model.ChannelType;
import com.newrelic.api.agent.Trace;
import java.util.Optional;

public interface EventIdResolver {
  Optional<Long> resolveEventId(LiveUpdatesChannel channel);

  Optional<Long> resolveEventId(ChannelType channelType, Long channelId);

  @Trace(metricName = "ResolveEvent", dispatcher = true)
  Optional<Long> resolveEventId(String rawChannel);
}
