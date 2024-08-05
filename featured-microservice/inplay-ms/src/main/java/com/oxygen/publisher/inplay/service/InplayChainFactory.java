package com.oxygen.publisher.inplay.service;

import static com.oxygen.publisher.inplay.context.InplaySocketMessages.*;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionType;
import com.fasterxml.jackson.databind.type.TypeFactory;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import com.oxygen.publisher.inplay.context.InplayMiddlewareContext;
import com.oxygen.publisher.model.*;
import com.oxygen.publisher.translator.AbstractWorker;
import com.oxygen.publisher.translator.DiagnosticService;
import com.oxygen.publisher.translator.RootWorker;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;
import lombok.Builder;
import lombok.Data;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;

@RequiredArgsConstructor
@Slf4j
public class InplayChainFactory extends AbstractInPlayChainFactory {

  @Getter @Setter private static InplayChainFactory inplayChainFactory;
  private final InplayMiddlewareContext inplayMiddlewareContext;
  private final DiagnosticService diagnosticService;
  private final ObjectMapper objectMapper;
  private static final Integer HR_CATEGORY_ID = 21;

  @Value("${newrelic.live.update.send.transaction.name}")
  private String liveUpdateTransactionName;

  @Override
  @RootWorker()
  public AbstractWorker getScheduledJob() {
    return workerVersion(new InplayCachedData());
  }

  @Override
  public DiagnosticService diagnosticService() {
    return diagnosticService;
  }

  /**
   * To create workers chain with a full flow of processes which can update the cache in middleware
   * context and subscribe on necessary topics. For Tests NOTES: mock cache object will be helpful
   * for verification changes for each step of processing the featured data.
   *
   * @param thisCache expected empty cache for following processes.
   * @return the first worker from the chain.
   */
  public final AbstractWorker<Void, String> workerVersion(InplayCachedData thisCache) {
    return and(
        thisCache,
        (thisWorker, model) ->
            inplayMiddlewareContext
                .inplayDataService()
                .getLastGeneration(
                    (String lastVersion) -> {
                      if (Objects.nonNull(lastVersion)) {
                        log.info("{} version of the InPlay data.", lastVersion);
                        if (inplayMiddlewareContext
                            .getInplayCachedData()
                            .getVersion()
                            .equals(lastVersion)) {
                          log.warn(
                              "{} version of the InPlay data didn't change from last run.",
                              lastVersion);
                          return;
                        }
                        thisCache.setVersion(lastVersion);
                        thisWorker.accept(lastVersion, () -> inplayDataWorker(thisCache));
                        thisWorker.accept(lastVersion, () -> sportsRibbonWorker(thisCache));
                        thisWorker.accept(lastVersion, () -> optimizeSportSegmentCache(thisCache));
                        thisWorker.accept(lastVersion, () -> virtualSportsWorker(thisCache));
                        inplayMiddlewareContext.applyWorkingCache(thisCache);
                      }
                    }));
  }

  protected final AbstractWorker<String, InPlayData> inplayDataWorker(InplayCachedData thisCache) {
    return and(
        thisCache,
        (thisWorker, version) ->
            inplayMiddlewareContext
                .inplayDataService()
                .getInPlayModel(
                    version,
                    (InPlayData inPlayData) -> {
                      // InplayDataService pass null if data consuming wasn't successful, so this is
                      // an expected state
                      // throw exception to avoid populating invalid/null data into cache, it's
                      // better
                      // to store old one instead of null
                      // TODO add some retry logic if failed to consume
                      if (Objects.isNull(inPlayData)) {
                        throw new IllegalStateException(
                            "Failed to consume InPlayModel. Stopping this chain execution.");
                      }
                      thisCache.setStructureWithoutStreamEvents(
                          inPlayData.getShallowCopyWithoutStreamEvents());
                      thisCache.setStructure(inPlayData);
                    }));
  }

  public final AbstractWorker<String, SportsRibbon> sportsRibbonWorker(InplayCachedData thisCache) {
    return and(
        thisCache,
        (thisWorker, version) ->
            inplayMiddlewareContext
                .inplayDataService()
                .getSportsRibbon(
                    version,
                    (SportsRibbon sportsRibbon) -> {
                      if (Objects.isNull(sportsRibbon)) {
                        throw new IllegalStateException(
                            "Failed to consume SportsRibbon. Stopping this chain execution.");
                      }
                      thisCache.setSportsRibbon(sportsRibbon);
                      SportsRibbon sportsRibbonWithLiveStreams = new SportsRibbon();
                      sportsRibbonWithLiveStreams.setItems(sportsRibbon.getItemsWithLiveStreams());
                      thisCache.setSportsRibbonWithLiveStreams(sportsRibbonWithLiveStreams);
                    }));
  }

  protected final AbstractWorker<String, InPlayCache> optimizeSportSegmentCache(
      InplayCachedData locker) {
    return and(
        locker,
        (thisWorker, version) ->
            inplayMiddlewareContext
                .inplayDataService()
                .getInPlayCache(
                    version,
                    (InPlayCache inPlayCache) -> {
                      if (Objects.isNull(inPlayCache)) {
                        throw new IllegalStateException(
                            "Failed to consume inPlayCache. Stopping this chain execution.");
                      }
                      final Map<String, InPlayByEventMarket> dist = locker.getPrimaryMarketCache();
                      inPlayCache
                          .getSportSegmentCaches()
                          .forEach(
                              (InPlayCache.SportSegmentCache chSegment) -> {
                                RawIndex rawIndex = chSegment.getStructuredKey();
                                if (chSegment.getSportSegment() != null) {
                                  chSegment
                                      .getSportSegment()
                                      .getEventsByTypeName()
                                      .forEach(
                                          typeSegment ->
                                              typeSegment.setEvents(
                                                  optimizeEvents(
                                                      dist, typeSegment.getEvents(), rawIndex)));
                                } else {
                                  chSegment.setModuleDataItem(
                                      optimizeEvents(
                                          dist, chSegment.getModuleDataItem(), rawIndex));
                                }
                              });
                      locker.setPrimaryMarketCache(dist);
                      thisWorker.accept(inPlayCache, () -> unpackInplayCache(locker));
                    }));
  }

  public final AbstractWorker<String, VirtualSportEvents> virtualSportsWorker(
      InplayCachedData thisCache) {

    return and(
        thisCache,
        (thisWorker, version) ->
            inplayMiddlewareContext
                .inplayDataService()
                .getVirtualSport(
                    version,
                    (List<VirtualSportEvents> virtualSportDtos) -> {
                      log.info("The current version for virtual sports is : " + version);
                      thisCache.getStructure().setVirtualSportList(virtualSportDtos);
                    }));
  }

  protected final AbstractWorker<InPlayCache, Collection<InPlayCache.SportSegmentCache>>
      unpackInplayCache(InplayCachedData locker) {
    return and(
        locker,
        (AbstractWorker<InPlayCache, Collection<InPlayCache.SportSegmentCache>> thisWorker,
            InPlayCache inPlayCache) -> {
          Map<RawIndex, InPlayCache.SportSegmentCache> sportSegments = new ConcurrentHashMap<>();
          Map<RawIndex, InPlayCache.SportSegmentCache> sportSegmentsWithEmptyTypes =
              new ConcurrentHashMap<>();
          inPlayCache.getSportSegmentCaches().stream()
              .filter(java.util.Objects::nonNull)
              .forEach(
                  (InPlayCache.SportSegmentCache sportSegmentCache) -> {
                    RawIndex thisIndex = sportSegmentCache.getStructuredKey();
                    sportSegments.put(thisIndex, sportSegmentCache);
                    if (sportSegmentCache.getSportSegment() != null) {
                      SportSegment sportSegmentWithEmptyTypes;
                      if (HR_CATEGORY_ID.equals(
                          sportSegmentCache.getSportSegment().getCategoryId())) {
                        sportSegmentWithEmptyTypes =
                            sportSegmentCache.getSportSegment().getCloneWithEmptyHRTypes();
                      } else {
                        sportSegmentWithEmptyTypes =
                            sportSegmentCache.getSportSegment().getCloneWithEmptyTypes();
                      }
                      sportSegmentsWithEmptyTypes.put(
                          thisIndex,
                          new InPlayCache.SportSegmentCache(
                              sportSegmentWithEmptyTypes,
                              null,
                              sportSegmentCache.getStructuredKey()));
                    }
                  });
          locker.getSportSegments().putAll(sportSegments);
          locker.getSportSegmentsWithEmptyTypes().putAll(sportSegmentsWithEmptyTypes);
        });
  }

  @RootWorker()
  public final AbstractWorker<String, String> inplayDataChanged() {
    // rebuild all cache
    final InplayCachedData thisCache = new InplayCachedData();
    return and(
        thisCache,
        (AbstractWorker<String, String> thisWorker, String generationId) -> {
          log.debug("Started Inplay data worker..");
          inplayMiddlewareContext
              .inplayDataService()
              .getInPlayModel(
                  generationId,
                  (InPlayData inPlayData) -> {
                    if (Objects.nonNull(inPlayData)) {
                      thisCache.setStructureWithoutStreamEvents(
                          inPlayData.getShallowCopyWithoutStreamEvents());
                      thisCache.setStructure(inPlayData);
                      thisCache.setVersion(generationId);
                      thisWorker.accept(generationId, () -> sportsRibbonWorker(thisCache));
                      thisWorker.accept(generationId, () -> optimizeSportSegmentCache(thisCache));
                      thisWorker.accept(generationId, () -> virtualSportsWorker(thisCache));
                      inplayMiddlewareContext.applyWorkingCache(thisCache);
                      clientCacheChangedNotifier().start(null);
                    }
                  });
        });
  }

  @RootWorker()
  public final AbstractWorker<String, SportsRibbon> sportsRibbonChanged() {
    final InplayCachedData thisCache = inplayMiddlewareContext.getInplayCachedData();
    return and(
        thisCache,
        (AbstractWorker<String, SportsRibbon> thisWorker, String generationId) -> {
          log.debug("Started Sports Ribbon worker..");
          inplayMiddlewareContext
              .inplayDataService()
              .getSportsRibbon(
                  generationId,
                  (SportsRibbon sportsRibbon) -> {
                    if (Objects.nonNull(sportsRibbon)) {
                      thisCache.setSportsRibbon(sportsRibbon);
                      SportsRibbon sportsRibbonWithLiveStreams = new SportsRibbon();
                      sportsRibbonWithLiveStreams.setItems(sportsRibbon.getItemsWithLiveStreams());
                      thisCache.setSportsRibbonWithLiveStreams(sportsRibbonWithLiveStreams);
                      log.debug(
                          "[InplayChainFactory: IN_PLAY_SPORTS_RIBBON_CHANGED ] for hash {} ",
                          sportsRibbon.hashCode());
                      inplayMiddlewareContext
                          .socketIOServer()
                          .getRoomOperations(IN_PLAY_SPORTS_RIBBON_CHANGED.messageId())
                          .sendEvent(IN_PLAY_SPORTS_RIBBON_CHANGED.messageId(), sportsRibbon);
                      inplayMiddlewareContext
                          .socketIOServer()
                          .getRoomOperations(IN_PLAY_LS_SPORTS_RIBBON_CHANGED.messageId())
                          .sendEvent(
                              IN_PLAY_LS_SPORTS_RIBBON_CHANGED.messageId(),
                              sportsRibbonWithLiveStreams);
                    }
                  });
        });
  }

  @RootWorker()
  public final AbstractWorker<String, List<VirtualSportEvents>> virtualSportsRibbonChanged() {
    final InplayCachedData thisCache = inplayMiddlewareContext.getInplayCachedData();
    return and(
        thisCache,
        (AbstractWorker<String, List<VirtualSportEvents>> thisWorker, String generationId) -> {
          log.debug("Started Virtual Sports worker..");
          inplayMiddlewareContext
              .inplayDataService()
              .getVirtualSport(
                  generationId,
                  (List<VirtualSportEvents> virtualSportDtos) -> {
                    thisCache.getStructure().setVirtualSportList(virtualSportDtos);
                    log.debug(
                        "[InplayChainFactory: VIRTUAL_SPORTS_RIBBON_CHANGED ] for hash {} ",
                        virtualSportDtos.hashCode());
                    inplayMiddlewareContext
                        .socketIOServer()
                        .getRoomOperations(GET_VIRTUAL_SPORTS_RIBBON_REQUEST.messageId())
                        .sendEvent(
                            GET_VIRTUAL_SPORTS_RIBBON_RESPONSE.messageId(), virtualSportDtos);
                  });
        });
  }

  @RootWorker()
  public final AbstractWorker<String, SportSegment> onSportSegmentsChanged() {
    final InplayCachedData thisCache = inplayMiddlewareContext.getInplayCachedData();
    return and(
        thisCache,
        (AbstractWorker<String, SportSegment> thisWorker, String generationId) -> {
          log.debug("Started Sport Segments worker..");
          try {
            // generationId looks like '208::16::STREAM_EVENT::First-Half Result'
            generationId = URLEncoder.encode(generationId, "UTF-8");
          } catch (UnsupportedEncodingException e) {
            log.error("Can't find UTF-8 encoding."); // UTF-8 is always supported
          }
          inplayMiddlewareContext
              .inplayDataService()
              .getSportSegment(
                  generationId,
                  (SportSegment sportSegment) -> {
                    if (Objects.nonNull(sportSegment)) {
                      final RawIndex key = new RawIndex(sportSegment);

                      thisCache
                          .getSportSegments()
                          .put(key, new InPlayCache.SportSegmentCache(sportSegment, null, key));
                      thisCache
                          .getSportSegmentsWithEmptyTypes()
                          .put(
                              key,
                              new InPlayCache.SportSegmentCache(
                                  sportSegment.getCloneWithEmptyTypes(), null, key));
                      thisCache
                          .getSportSegments()
                          .putAll(
                              sportSegment.getEventsByTypeName().stream()
                                  .collect(
                                      Collectors.toMap(
                                          typeSegment ->
                                              key.cloneToType(
                                                  Integer.parseInt(typeSegment.getTypeId())),
                                          (TypeSegment typeSegment) -> {
                                            RawIndex typeIdIndex =
                                                key.cloneToType(
                                                    Integer.parseInt(typeSegment.getTypeId()));
                                            typeSegment
                                                .getEvents()
                                                .forEach(
                                                    (ModuleDataItem event) -> {
                                                      cropMarkets(typeIdIndex, event);
                                                      String prMarketIndex =
                                                          createPRMarketCacheIndex(
                                                              event.getId(), event.getMarkets());
                                                      InPlayByEventMarket eventByMarket =
                                                          thisCache
                                                              .getPrimaryMarketCache()
                                                              .get(prMarketIndex);
                                                      if (eventByMarket == null) {
                                                        eventByMarket = new InPlayByEventMarket();
                                                        thisCache
                                                            .getPrimaryMarketCache()
                                                            .put(prMarketIndex, eventByMarket);
                                                      }
                                                      eventByMarket.setModuleDataItem(event);
                                                      eventByMarket.addCacheRef(typeIdIndex);
                                                      eventByMarket.setPrimaryMarkets(
                                                          event.getPrimaryMarkets());
                                                      event.setPrimaryMarkets(null);
                                                    });
                                            return new InPlayCache.SportSegmentCache(
                                                null, typeSegment.getEvents(), typeIdIndex);
                                          })));
                    }
                  });
        });
  }

  public void processLiveUpdate(String eventId, String payload) {
    try {
      // increments live updates counter.
      inplayMiddlewareContext.getInplayCachedData().getTicksMetrics().incLiveUpdatesTickCounter();
      BaseObject baseObject = objectMapper.readValue(payload, BaseObject.class);
      // added payload for live updates cache.
      inplayMiddlewareContext.getInplayCachedData().addLiveUpdatesCache(baseObject);
      // emit room updates.
      track(baseObject, eventId);
      inplayMiddlewareContext
          .socketIOServer()
          .getRoomOperations(eventId)
          .sendEvent(eventId, baseObject);
      inplayChainFactory
          .reflectLiveUpdates(baseObject.getEvent().getEventId().toString())
          .start(baseObject);
    } catch (Exception e) {
      log.error("While parsing", e);
      NewRelic.noticeError(e);
    }
  }

  @Trace(dispatcher = true)
  private void track(BaseObject baseObject, String room) {
    NewRelic.setTransactionName(null, liveUpdateTransactionName + baseObject.getType());
    log.debug("[InplayChainFactory: liveUpdates ] room: {} -> {}", room, baseObject.hashCode());
  }

  protected AbstractWorker<String, Void> moveToNextPRMarket(String eventId) {
    return and(
        eventId,
        (AbstractWorker<String, Void> thisWorker, String prMarketIndex) -> {
          Map<String, InPlayByEventMarket> primaryMarketCache =
              inplayMiddlewareContext.getInplayCachedData().getPrimaryMarketCache();
          InPlayByEventMarket oldEventMarket = primaryMarketCache.get(prMarketIndex);
          if (!oldEventMarket.hasIndexForLevel(0) || !oldEventMarket.hasIndexForLevel(1)) {
            log.info(
                "[ InplayChainFactory:moveToNextPRMarket ] this market is not primary. {}",
                prMarketIndex);
          }
          String marketId = getNextPrimaryMarketId(oldEventMarket);
          // if live update with info that the last primary market is suspended was processed after
          // inplay
          // structure/sport category was updated (so no following primary markets)
          if (marketId == null) {
            log.info(
                "[ InplayChainFactory:moveToNextPRMarket ] the next primary market didn't found. Old {} New "
                    + "NULL",
                prMarketIndex);
            return;
          }
          String newPRMarketIndex = createPRMarketCacheIndex(eventId, marketId);
          if (!primaryMarketCache.containsKey(newPRMarketIndex)) {
            log.error(
                "[ InplayChainFactory:moveToNextPRMarket ] New primary market not found EventId::MarketId {}",
                newPRMarketIndex);
            return;
          }
          InPlayByEventMarket newEventMarket = primaryMarketCache.get(newPRMarketIndex);
          final Set<RawIndex> refIndexes = oldEventMarket.getCacheRefsByLevel(0);
          refIndexes.addAll(oldEventMarket.getCacheRefsByLevel(1));
          refIndexes.forEach(
              (RawIndex rawIndex) -> {
                Map<RawIndex, InPlayCache.SportSegmentCache> cacheMap =
                    inplayMiddlewareContext.getInplayCachedData().getSportSegments();
                ModuleDataItem oldModuleDataItem = oldEventMarket.getModuleDataItem();
                if (rawIndex.getLevel() == 0) {
                  cacheMap.get(rawIndex).getSportSegment().getEventsByTypeName().stream()
                      .filter(
                          typeSegment ->
                              typeSegment.getTypeId().equals(String.valueOf(rawIndex.getTypeId())))
                      .findAny()
                      .ifPresent(
                          typeSegment ->
                              typeSegment
                                  .getEvents()
                                  .set(
                                      typeSegment.getEvents().indexOf(oldModuleDataItem),
                                      newEventMarket.getModuleDataItem()));
                } else {
                  resetEventMarket(newEventMarket, rawIndex, cacheMap, oldModuleDataItem);
                }
                oldEventMarket.getCacheRefs().removeAll(refIndexes);
                newEventMarket.getCacheRefs().addAll(refIndexes);
              });
        });
  }

  protected void resetEventMarket(
      InPlayByEventMarket newEventMarket,
      RawIndex rawIndex,
      Map<RawIndex, InPlayCache.SportSegmentCache> cacheMap,
      ModuleDataItem oldModuleDataItem) {
    InPlayCache.SportSegmentCache sportSegmentCache = cacheMap.get(rawIndex);
    if (sportSegmentCache != null) {
      List<ModuleDataItem> modules = sportSegmentCache.getModuleDataItem();
      int oldModuleIndex = modules.indexOf(oldModuleDataItem);
      if (oldModuleIndex >= 0 && oldModuleIndex < modules.size()) {
        modules.set(oldModuleIndex, newEventMarket.getModuleDataItem());
      } else {
        log.warn(
            "[ InplayChainFactory:moveToNextPRMarket ] "
                + "Event market module data not found in cache map by rawIndex {}. "
                + "Module name: {}, Module id: {}",
            rawIndex,
            oldModuleDataItem.getName(),
            oldModuleDataItem.getId());
      }
    }
  }

  @RootWorker
  public AbstractWorker<BaseObject, String> reflectLiveUpdates(String eventId) {
    return and(
        eventId,
        (AbstractWorker<BaseObject, String> thisWorker, BaseObject baseObject) -> {
          if ("EVMKT".equals(baseObject.getType())
              && ("N".equals(baseObject.getEvent().getMarket().getDisplayed())
                  || "S".equals(baseObject.getEvent().getMarket().getStatus()))) {
            Map<String, InPlayByEventMarket> primaryMarketCache =
                inplayMiddlewareContext.getInplayCachedData().getPrimaryMarketCache();
            String thisMarketKey =
                createPRMarketCacheIndex(
                    baseObject.getEvent().getEventId().toString(),
                    baseObject.getEvent().getMarket().getMarketId().toString());
            if (primaryMarketCache.containsKey(thisMarketKey)) {
              thisWorker.accept(thisMarketKey, () -> moveToNextPRMarket(eventId));
            }
          }
        });
  }

  /**
   * Notify relation on IN_PLAY_STRUCTURE_CHANGED event.
   *
   * @return worker which can do this.
   */
  protected AbstractWorker<Void, Void> clientCacheChangedNotifier() {
    return and(
        IN_PLAY_STRUCTURE_CHANGED.messageId(),
        (AbstractWorker<Void, Void> thisWorker, Void model) -> {
          log.debug(
              "[InplayChainFactory: IN_PLAY_STRUCTURE_CHANGED ] for room {} ",
              IN_PLAY_STRUCTURE_CHANGED.messageId());
          inplayMiddlewareContext
              .socketIOServer()
              .getRoomOperations(IN_PLAY_STRUCTURE_CHANGED.messageId())
              .sendEvent(
                  IN_PLAY_STRUCTURE_CHANGED.messageId(),
                  inplayMiddlewareContext.getInplayCachedData().getStructureWithoutStreamEvents());
          inplayMiddlewareContext
              .socketIOServer()
              .getRoomOperations(IN_PLAY_LS_STRUCTURE_CHANGED.messageId())
              .sendEvent(
                  IN_PLAY_LS_STRUCTURE_CHANGED.messageId(),
                  inplayMiddlewareContext.getInplayCachedData().getStructure());
        });
  }

  @RootWorker
  public final AbstractWorker<String, String> processCompetitionChanges() {
    return and(
        IN_PLAY_SPORT_COMPETITION_CHANGED.messageId(),
        (AbstractWorker<String, String> thisWorker, String model) -> {
          List<SportCompetitionChanges> changes = getSportCompetitionChanges(model);
          changes.stream()
              .map(SportCompetitionChanges::getGenerationId)
              .filter(Objects::nonNull)
              .findAny()
              .ifPresent(
                  (String generationId) -> {
                    InplayCachedData inplayCachedData =
                        inplayMiddlewareContext.getInplayCachedData();
                    if (!inplayCachedData.getVersion().equals(generationId)) {
                      NewRelic.incrementCounter("Custom/refreshSportCompetitions");
                      thisWorker.accept(
                          generationId, () -> optimizeSportSegmentCache(inplayCachedData));
                    }
                  });
          thisWorker.accept(
              IN_PLAY_SPORT_COMPETITION_CHANGED.messageId(),
              () -> notifyCompetitionChanged(changes));
        });
  }

  @SneakyThrows
  private List<SportCompetitionChanges> getSportCompetitionChanges(String model) {
    try {
      CollectionType competitionChangesListType =
          TypeFactory.defaultInstance()
              .constructCollectionType(ArrayList.class, SportCompetitionChanges.class);
      return objectMapper.readValue(model, competitionChangesListType);
    } catch (JsonProcessingException e) {
      log.error("Failed too deserialize SportCompetitionChanges", e);
      throw e;
    }
  }

  private AbstractWorker<String, Void> notifyCompetitionChanged(
      List<SportCompetitionChanges> changes) {
    return and(
        IN_PLAY_SPORT_COMPETITION_CHANGED.messageId(),
        (thisWorker, generation) ->
            changes.forEach(
                (SportCompetitionChanges diff) -> {
                  String room =
                      IN_PLAY_SPORT_COMPETITION_CHANGED.messageId() + "::" + diff.getKey();
                  log.info(
                      "[InplayChainFactory: IN_PLAY_SPORT_COMPETITION_CHANGED ] for room {}, generation {} ",
                      room,
                      diff.getGenerationId());
                  inplayMiddlewareContext
                      .socketIOServer()
                      .getRoomOperations(room)
                      .sendEvent(
                          room,
                          SportCompetitionChanged.builder()
                              .added(diff.getAdded())
                              .changed(diff.getChanged())
                              .removed(diff.getRemoved())
                              .build());
                }));
  }

  @Data
  @Builder
  public static class SportCompetitionChanged {
    private Map<String, TypeSegment> added;
    private Set<String> changed;
    private Set<String> removed;
  }
}
