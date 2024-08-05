package com.oxygen.publisher.model;

import com.google.common.cache.Cache;
import com.google.common.cache.CacheBuilder;
import com.newrelic.api.agent.NewRelic;
import com.oxygen.publisher.api.AbstractCachedData;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.extern.slf4j.Slf4j;

/** Created by Aliaksei Yarotski on 3/1/18. */
@Data
@EqualsAndHashCode(callSuper = false)
@Slf4j
public class InplayCachedData extends AbstractCachedData {

  private InPlayData structureWithoutStreamEvents;

  private String version = "InplayCachedData";
  private InPlayData structure; // populated from inplay_structure imap // applyWorkingCache
  private SportsRibbon sportsRibbon; // populated from inplay_sports_ribbon
  private SportsRibbon sportsRibbonWithLiveStreams;
  // populated from inplay_cached_structure, updated from inplay_module on sportSegments update
  // key = getCategoryId() + "::" + getTopLevelType() + "::" + [getMarketSelector()] +
  // [typeSegment.getTypeId()]
  private Map<RawIndex, InPlayCache.SportSegmentCache> sportSegments;
  private Map<RawIndex, InPlayCache.SportSegmentCache> sportSegmentsWithEmptyTypes;
  private Map<String, InPlayByEventMarket> primaryMarketCache;

  public InplayCachedData() {
    sportSegments = new ConcurrentHashMap();
    sportSegmentsWithEmptyTypes = new ConcurrentHashMap<>();
    primaryMarketCache = new ConcurrentHashMap();
  }

  // payload from LiveServer
  private final Cache<String, ConcurrentHashMap<LiveRawIndex, BaseObject>> liveUpdatesCache =
      CacheBuilder.newBuilder()
          .maximumSize(20000)
          .expireAfterWrite(3, TimeUnit.HOURS)
          .initialCapacity(10000)
          .build();

  public void addLiveUpdatesCache(BaseObject baseObject) {
    String roomName = baseObject.getEvent().getEventId().toString();
    LiveRawIndex index =
        LiveRawIndex.builder()
            .eventId(baseObject.getEvent().getEventId().toString())
            .updatedType(baseObject.getType())
            .subjectId(LiveRawIndex.crateSubjectId(baseObject))
            .build();
    try {
      ConcurrentHashMap<LiveRawIndex, BaseObject> thisPayload =
          liveUpdatesCache.getIfPresent(roomName);
      if (thisPayload == null) {
        thisPayload = new ConcurrentHashMap<>();
        thisPayload.put(index, baseObject);
      } else {
        thisPayload.put(index, baseObject);
      }
      liveUpdatesCache.put(index.getEventId(), thisPayload);
    } catch (Exception e) {
      log.error("[InplayCachedData:addLiveUpdatesCache]", e);
      NewRelic.noticeError(e);
    }
  }

  public BaseObject[] getPayload(String roomName) {
    Map<LiveRawIndex, BaseObject> thisPayload = this.liveUpdatesCache.getIfPresent(roomName);
    if (thisPayload != null) {
      return thisPayload.values().toArray(new BaseObject[thisPayload.size()]);
    }
    return null;
  }

  @Override
  public String getEntityGUID() {
    return version;
  }

  @Override
  public boolean isEmpty() {
    return structure == null;
  }
}
