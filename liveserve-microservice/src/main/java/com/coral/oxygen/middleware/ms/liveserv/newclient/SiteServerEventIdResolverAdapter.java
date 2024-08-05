package com.coral.oxygen.middleware.ms.liveserv.newclient;

import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;
import com.coral.oxygen.middleware.ms.liveserv.impl.OldEventIdResolver;
import com.coral.oxygen.middleware.ms.liveserv.model.ChannelType;
import com.google.common.cache.Cache;
import com.google.common.cache.CacheBuilder;
import java.util.Optional;
import java.util.concurrent.TimeUnit;

public class SiteServerEventIdResolverAdapter implements EventIdResolver {

  private final OldEventIdResolver eventIdResolver;
  private final Cache<String, Long> resolvedEvents;

  public SiteServerEventIdResolverAdapter(
      OldEventIdResolver eventIdResolver,
      int sizeOfResolvedEventsCache,
      int ttlOfResolvedEventsCache) {
    this.eventIdResolver = eventIdResolver;
    resolvedEvents =
        CacheBuilder.newBuilder()
            .maximumSize(sizeOfResolvedEventsCache)
            .expireAfterAccess(ttlOfResolvedEventsCache, TimeUnit.SECONDS)
            .build();
  }

  @Override
  public Optional<Long> resolveEventId(LiveUpdatesChannel channel) {
    return resolveEventId(channel.getKeyValue());
  }

  @Override
  public Optional<Long> resolveEventId(ChannelType channelType, Long channelId) {
    return resolveEventId(new LiveUpdatesChannel(channelType, String.valueOf(channelId)));
  }

  @Override
  public Optional<Long> resolveEventId(String rawChannel) {
    Long eventId = resolvedEvents.getIfPresent(rawChannel);
    if (eventId == null) {
      try {
        eventId = eventIdResolver.resolveEventId(rawChannel);
        resolvedEvents.put(rawChannel, eventId);
      } catch (ServiceException e) {
        return Optional.empty();
      }
    }
    return Optional.ofNullable(eventId);
  }
}
