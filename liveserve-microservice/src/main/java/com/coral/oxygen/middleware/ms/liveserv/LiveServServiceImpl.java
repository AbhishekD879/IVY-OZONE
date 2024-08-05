package com.coral.oxygen.middleware.ms.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStatsOld;
import com.coral.oxygen.middleware.ms.liveserv.newclient.EventIdResolver;
import com.coral.oxygen.middleware.ms.liveserv.newclient.LiveUpdatesChannel;
import com.coral.oxygen.middleware.ms.liveserv.newclient.LiveUpdatesChannelFactory;
import com.coral.oxygen.middleware.ms.liveserv.newclient.chunked.ChunkedLiveUpdates;
import com.newrelic.api.agent.Trace;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class LiveServServiceImpl implements LiveServService {
  private final ChunkedLiveUpdates chunkedLiveUpdates;
  private final EventIdResolver eventIdResolver;

  public LiveServServiceImpl(
      ChunkedLiveUpdates chunkedLiveUpdates, EventIdResolver eventIdResolver) {
    this.chunkedLiveUpdates = chunkedLiveUpdates;
    this.eventIdResolver = eventIdResolver;
  }

  @Trace(metricName = "subscribe", dispatcher = true)
  @Override
  public void subscribe(String channel) {
    Objects.requireNonNull(channel);
    chunkedLiveUpdates.subscribeOnItem(parseLiveUpdatesChannel(channel));
  }

  private LiveUpdatesChannel parseLiveUpdatesChannel(String channel) {
    return LiveUpdatesChannelFactory.fromString(channel);
  }

  @Trace(metricName = "unsubscribe", dispatcher = true)
  @Override
  public void unsubscribe(String channel) {
    log.info("[LS] UnSubscribe on channel {}", channel);
    chunkedLiveUpdates.unsubscribe(parseLiveUpdatesChannel(channel));
  }

  @Override
  public Map<String, SubscriptionStats> getSubscriptions() {
    return chunkedLiveUpdates.getPayloadItems().entrySet().stream()
        .collect(Collectors.toMap(e -> e.getValue().getKeyValue(), e -> toSubStats(e.getValue())));
  }

  private SubscriptionStats toSubStats(LiveUpdatesChannel value) {
    String rawChannel = value.getKeyValue();
    return new SubscriptionStatsOld(
        rawChannel, eventIdResolver.resolveEventId(rawChannel).orElse(0L));
  }
}
