package com.oxygen.publisher.sportsfeatured.model;

import com.google.common.cache.Cache;
import com.google.common.cache.CacheBuilder;
import com.google.common.cache.RemovalCause;
import com.google.common.cache.RemovalNotification;
import com.newrelic.api.agent.NewRelic;
import com.oxygen.publisher.api.AbstractCachedData;
import com.oxygen.publisher.model.BaseObject;
import com.oxygen.publisher.model.LiveRawIndex;
import com.oxygen.publisher.sportsfeatured.model.module.AbstractFeaturedModule;
import java.time.Duration;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;

/** Created by Aliaksei Yarotski on 2/26/18. */
@EqualsAndHashCode(callSuper = true)
@Slf4j
@Getter
public class SportsCachedData extends AbstractCachedData {

  private static final Duration MODULES_CACHE_TTL = Duration.ofHours(3);
  private static final int MODULES_CACHE_INITIAL_SIZE = 100;
  private static final int MODULES_CACHE_MAX_SIZE = 1000;

  public static final Duration PRIMARY_MARKET_CACHE_TTL = Duration.ofMinutes(15);
  public static final int PRIMARY_MARKET_CACHE_INITIAL_SIZE = 250;
  public static final int PRIMARY_MARKET_CACHE_MAX_SIZE = 25000;

  public static final Duration LIVE_UPDATES_CACHE_TTL = Duration.ofMinutes(15);
  public static final int LIVE_UPDATES_CACHE_MAX_SIZE = 20000;
  public static final int SPORT_PAGE_CACHE_INITIAL_SIZE = 1000;
  public static final int SPORT_PAGE_CACHE_MAX_SIZE = 2000;

  private volatile long generation;
  private final Map<PageRawIndex, Long> generationMap;
  private final Cache<PageRawIndex, FeaturedModel> structureMap;
  private final Cache<ModuleRawIndex, AbstractFeaturedModule<?>> moduleMap;
  private final Cache<String, FeaturedByEventMarket> primaryMarketCache;
  private final Cache<String, Map<LiveRawIndex, BaseObject>> liveUpdatesCache;

  private final Cache<String, PageRawIndex> sportPageMap;

  public SportsCachedData(int structureCacheMaxSize, long structureTtlSeconds) {
    this.generation = -1;
    this.generationMap = new ConcurrentHashMap<>();
    this.structureMap =
        CacheBuilder.newBuilder()
            .maximumSize(structureCacheMaxSize)
            .expireAfterWrite(structureTtlSeconds, TimeUnit.SECONDS)
            .initialCapacity(structureCacheMaxSize)
            .removalListener(
                (RemovalNotification<PageRawIndex, FeaturedModel> e) -> {
                  if (RemovalCause.REPLACED != e.getCause()) {
                    generationMap.remove(e.getKey());
                  }
                })
            .build();
    moduleMap =
        CacheBuilder.newBuilder()
            .maximumSize(MODULES_CACHE_MAX_SIZE)
            .expireAfterWrite(MODULES_CACHE_TTL)
            .initialCapacity(MODULES_CACHE_INITIAL_SIZE)
            .build();
    this.primaryMarketCache =
        CacheBuilder.newBuilder()
            // max amount of events
            .maximumSize(PRIMARY_MARKET_CACHE_MAX_SIZE)
            .expireAfterWrite(PRIMARY_MARKET_CACHE_TTL)
            .initialCapacity(PRIMARY_MARKET_CACHE_INITIAL_SIZE)
            .build();
    this.liveUpdatesCache =
        CacheBuilder.newBuilder()
            // payload from LiveServer
            .maximumSize(LIVE_UPDATES_CACHE_MAX_SIZE)
            .expireAfterWrite(LIVE_UPDATES_CACHE_TTL)
            .initialCapacity(LIVE_UPDATES_CACHE_MAX_SIZE)
            .build();

    this.sportPageMap =
        CacheBuilder.newBuilder()
            .maximumSize(SPORT_PAGE_CACHE_MAX_SIZE)
            .initialCapacity(SPORT_PAGE_CACHE_INITIAL_SIZE)
            .build();
  }

  @Override
  public String getEntityGUID() {
    // TODO: better to lock on PageType::sportId
    // right now can't get rid of generation b/c not sure how to lock on PageType::sportId
    return String.valueOf(generation);
  }

  public void insertSportPageData(Map<String, PageRawIndex> sportPages) {

    this.sportPageMap.putAll(sportPages);
  }

  public Map<String, PageRawIndex> getSportPageData() {

    return sportPageMap.asMap();
  }

  public void removeSportIdFromSportPageMapCache(final String sportId) {

    Optional.ofNullable(sportPageMap.getIfPresent(sportId))
        .ifPresent(
            pageRawIndex -> sportPageMap.invalidate(String.valueOf(pageRawIndex.getSportId())));
  }

  public Map<String, FeaturedByEventMarket> getPrimaryMarketCache() {
    return primaryMarketCache.asMap();
  }

  public void addLiveUpdatesCache(BaseObject baseObject) {
    // PRICE changes are handled by FEATURED_MODULE_CONTENT_CHANGED updates
    if ("PRICE".equals(baseObject.getType())) {
      return;
    }
    try {
      LiveRawIndex index =
          LiveRawIndex.builder()
              .eventId(baseObject.getEvent().getEventId().toString())
              .updatedType(baseObject.getType())
              .subjectId(LiveRawIndex.crateSubjectId(baseObject))
              .build();
      String eventId = index.getEventId();
      Map<LiveRawIndex, BaseObject> byEvent = liveUpdatesCache.getIfPresent(eventId);
      if (byEvent == null) {
        byEvent = initEventLiveUpdateMap(eventId);
      }
      byEvent.put(index, baseObject);
      liveUpdatesCache.put(index.getEventId(), byEvent);
    } catch (Exception e) {
      log.error("[FeaturedCachedData:addLiveUpdatesCache]", e);
      NewRelic.noticeError(e);
    }
  }

  private Map<LiveRawIndex, BaseObject> initEventLiveUpdateMap(String eventId) {
    Map<LiveRawIndex, BaseObject> byEvent;
    synchronized (eventId.intern()) {
      byEvent = liveUpdatesCache.getIfPresent(eventId);
      if (byEvent == null) {
        byEvent = new ConcurrentHashMap<>();
        liveUpdatesCache.put(eventId, byEvent);
      }
    }
    return byEvent;
  }

  public BaseObject[] getPayload(String roomName) {
    Map<LiveRawIndex, BaseObject> thisPayload = this.liveUpdatesCache.getIfPresent(roomName);
    if (thisPayload != null) {
      return thisPayload.values().toArray(new BaseObject[0]);
    }
    return null;
  }

  public FeaturedModel getStructure(PageRawIndex pageId) {
    return structureMap.getIfPresent(pageId);
  }

  public Optional<Map.Entry<ModuleRawIndex, AbstractFeaturedModule<?>>> findModuleById(
      String moduleId) {
    return moduleMap.asMap().entrySet().stream()
        .filter(entity -> entity.getKey().getModuleId().equals(moduleId))
        .findAny();
  }

  /**
   * Create / Update page in existing cache.
   *
   * @param newPageData updating page data.
   */
  public void updatePage(PageCacheUpdate newPageData) {
    PageRawIndex pageRawIndex = PageRawIndex.fromGenerationKey(newPageData.getPageVersion());

    if (this.generationMap.containsKey(pageRawIndex)
        && newPageData.getPageVersion().getVersion() < this.generationMap.get(pageRawIndex)) {
      log.error(
          "Rejected tye for applying out-date page model. Actual version: {}, New version {}, pageId {}",
          this.generationMap.get(pageRawIndex),
          newPageData.getPageVersion().getVersion(),
          pageRawIndex);
    } else {
      this.generation = newPageData.getPageVersion().getVersion();
      this.generationMap.put(pageRawIndex, newPageData.getPageVersion().getVersion());
      this.structureMap.put(
          PageRawIndex.fromModel(newPageData.getPageModel()), newPageData.getPageModel());
      this.moduleMap.putAll(newPageData.getModuleMap());
      this.primaryMarketCache.putAll(newPageData.getPrimaryMarketCache());
    }
  }

  @Override
  public boolean isEmpty() {
    return structureMap.size() == 0;
  }

  public void updatePrimaryMarketCache(Map<String, FeaturedByEventMarket> optimizeModule) {
    primaryMarketCache.putAll(optimizeModule);
  }

  public AbstractFeaturedModule<?> getModuleIfPresent(ModuleRawIndex moduleRawIndex) {
    return moduleMap.getIfPresent(moduleRawIndex);
  }

  public <T extends AbstractFeaturedModule<?>> void updateModule(
      ModuleRawIndex moduleRawIndex, T module) {
    moduleMap.put(moduleRawIndex, module);
  }
}
