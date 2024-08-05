package com.coral.oxygen.middleware.ms.liveserv.impl.redis;

import com.coral.oxygen.middleware.ms.liveserv.ChannelUnsubcribeEvent;
import com.coral.oxygen.middleware.ms.liveserv.model.CachedChannel;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

@Service
public class RedisCacheService {

  private final SubscriptionCache subscriptionCache;

  @Autowired
  public RedisCacheService(SubscriptionCache subscriptionCache) {
    this.subscriptionCache = subscriptionCache;
  }

  @Async
  public void cacheSubscription(String channel) {
    subscriptionCache.save(new CachedChannel(channel));
  }

  public List<String> getAllSubscription() {
    List<CachedChannel> cachedChannels = subscriptionCache.findAll();

    return cachedChannels.stream()
        .filter(Objects::nonNull)
        .map(CachedChannel::getChannel)
        .collect(Collectors.toList());
  }

  @Async
  @EventListener
  public void onChannelUnsubscribe(ChannelUnsubcribeEvent channelUnsubcribeEvent) {
    subscriptionCache.deleteById(channelUnsubcribeEvent.getLiveServChannel());
  }
}
