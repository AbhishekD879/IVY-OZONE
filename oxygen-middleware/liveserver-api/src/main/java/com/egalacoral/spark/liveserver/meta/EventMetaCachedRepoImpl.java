package com.egalacoral.spark.liveserver.meta;

import com.github.benmanes.caffeine.cache.Cache;
import java.math.BigInteger;
import java.util.Optional;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
public class EventMetaCachedRepoImpl implements EventMetaInfoCachedRepository {
  private final Cache<BigInteger, EventMetaInfo> eventMetaInfoCache;

  @Override
  public void putByEventId(BigInteger eventId, EventMetaInfo eventMetaInfo) {
    eventMetaInfoCache.put(eventId, eventMetaInfo);
  }

  @Override
  public void putBySelectionId(BigInteger selectionId, EventMetaInfo eventMetaInfo) {
    eventMetaInfoCache.put(selectionId, eventMetaInfo);
  }

  @Override
  public void putByMarketId(BigInteger marketId, EventMetaInfo eventMetaInfo) {
    eventMetaInfoCache.put(marketId, eventMetaInfo);
  }

  @Override
  public Optional<EventMetaInfo> getBySelectionId(BigInteger selectionId) {
    return Optional.ofNullable(eventMetaInfoCache.getIfPresent(selectionId));
  }

  @Override
  public Optional<EventMetaInfo> getByMarketId(BigInteger marketId) {
    return Optional.ofNullable(eventMetaInfoCache.getIfPresent(marketId));
  }

  @Override
  public Optional<EventMetaInfo> getByEventId(BigInteger eventId) {
    return Optional.ofNullable(eventMetaInfoCache.getIfPresent(eventId));
  }

  protected Cache<BigInteger, EventMetaInfo> getEventMetaInfoCache() {
    return eventMetaInfoCache;
  }
}
