package com.oxygen.publisher.sportsfeatured.service;

import static com.oxygen.publisher.sportsfeatured.context.SportsSocketMessages.FEATURED_STRUCTURE_CHANGED;
import static com.oxygen.publisher.sportsfeatured.util.SportsHelper.HASH;

import com.corundumstudio.socketio.BroadcastOperations;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import com.oxygen.publisher.model.BaseObject;
import com.oxygen.publisher.model.OutputMarket;
import com.oxygen.publisher.model.OutputOutcome;
import com.oxygen.publisher.sportsfeatured.context.SportsMiddlewareContext;
import com.oxygen.publisher.sportsfeatured.context.SportsSessionContext;
import com.oxygen.publisher.sportsfeatured.model.*;
import com.oxygen.publisher.sportsfeatured.model.module.*;
import com.oxygen.publisher.sportsfeatured.model.module.data.AbstractModuleData;
import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData;
import com.oxygen.publisher.sportsfeatured.model.module.data.FanBetsConfig;
import com.oxygen.publisher.sportsfeatured.model.module.data.TeamBetsConfig;
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.SportSegment;
import com.oxygen.publisher.sportsfeatured.util.SegmentedFeaturedModelHelper;
import com.oxygen.publisher.sportsfeatured.visitor.SocketIoRoomSubscriber;
import com.oxygen.publisher.translator.AbstractWorker;
import com.oxygen.publisher.translator.DiagnosticService;
import com.oxygen.publisher.translator.RootWorker;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;
import org.springframework.beans.factory.annotation.Value;

/** Created by Aliaksei Yarotski on 12/29/17. */
@RequiredArgsConstructor
@Slf4j
@SuppressWarnings("java:S6201")
public class SportsChainFactory extends AbstractSportsChainFactory {

  @Getter @Setter private static SportsChainFactory featuredChainFactory;

  private final SportsMiddlewareContext featuredMiddlewareContext;
  private final ObjectMapper objectMapper;
  private final DiagnosticService diagnosticService;
  private final SportsSessionContext sportsSessionContext;
  public static final int FANZONE_PAGE_ID = 160;

  private static final int FEATURED_COLLAPSED_MODULES_TIMEOUT = 2;
  private CountDownLatch lockBetweenWorkers;

  @Value("${newrelic.live.update.send.transaction.name}")
  private String liveUpdateTransactionName;

  private static final String UNIVERSAL_SEGMENT = "Universal";

  @Override
  protected SportsMiddlewareContext getContext() {
    return featuredMiddlewareContext;
  }

  /**
   * To create workers chain with a full flow of processes which can update the cache in middleware
   * context and subscribe on necessary topics. For Tests NOTES: mock cache object will be helpful
   * for verification changes for each step of processing the featured data.
   *
   * @return the first worker from the chain.
   */
  public final AbstractWorker<Void, PageRawIndex.GenerationKey> workerVersion() {
    return and(
        "GET_VERSION",
        (thisWorker, model) ->
            featuredMiddlewareContext
                .featuredService()
                .getLastGeneration(
                    genIds -> {
                      if (CollectionUtils.isNotEmpty(genIds)) {
                        genIds.parallelStream()
                            .forEach(pageGenId -> thisWorker.accept(pageGenId, this::processPage));
                      }
                    }));
  }

  protected final AbstractWorker<PageRawIndex.GenerationKey, FeaturedModel> processPage() {
    return and(
        "PROCESS_PAGE",
        (thisWorker, pageGenId) -> {
          log.debug("{} version of the model.", pageGenId);
          PageCacheUpdate newPageCache = new PageCacheUpdate(pageGenId);
          structureWorker(newPageCache).start(null);
        });
  }

  public final AbstractWorker<Void, PageRawIndex.GenerationKey> structureWorker(
      final PageCacheUpdate thisPageData) {
    return and(
        thisPageData,
        (thisWorker, empty) ->
            featuredMiddlewareContext
                .featuredService()
                .getFeaturedPagesStructure(
                    thisPageData.getPageVersion().toString(),
                    page -> {
                      if (Objects.nonNull(page)) {
                        thisPageData.setPageModel(page);
                        thisWorker.accept(thisPageData.getPageVersion(), this::populateModules);

                        // Need to wait until all collapsed modules are processed
                        try {
                          boolean allWorkersDone =
                              lockBetweenWorkers.await(
                                  FEATURED_COLLAPSED_MODULES_TIMEOUT, TimeUnit.SECONDS);
                          if (!allWorkersDone) {
                            log.warn(
                                "lockBetweenWorkers CountDownLatch waiting time elapsed before the count reached zero");
                          }
                        } catch (Exception e) {
                          log.error("StructureWorker CountDownLatch exception {0}", e);
                        }
                        featuredMiddlewareContext.registerNewPageId(PageRawIndex.fromModel(page));
                        featuredMiddlewareContext.applyWorkingCache(thisPageData);
                      }
                    }));
  }

  protected final AbstractWorker<
          PageRawIndex.GenerationKey, AbstractFeaturedModule<AbstractModuleData>>
      populateModules() {
    return and(
        "POPULATE_MODULES",
        (thisWorker, pageGeneration) -> {
          log.info("Modules worker started.");
          final PageCacheUpdate thisPageData = (PageCacheUpdate) thisWorker.getThisContext();
          thisPageData.setPrimaryMarketCache(
              new HashMap<>(
                  featuredMiddlewareContext.getFeaturedCachedData().getPrimaryMarketCache()));
          thisPageData.setModuleMap(new HashMap<>());

          List<? extends AbstractFeaturedModule<?>> eventsModules =
              thisPageData.getPageModel().getModules();

          int numberOfCollapsedModules =
              (int)
                  eventsModules.stream().filter(m -> CollectionUtils.isEmpty(m.getData())).count();
          lockBetweenWorkers = new CountDownLatch(numberOfCollapsedModules);

          if (CollectionUtils.isEmpty(eventsModules)) {
            log.debug("POPULATE_MODULES no modules for this page {} ", thisWorker.getChainId());
            return;
          }

          for (AbstractFeaturedModule<? extends AbstractModuleData> module : eventsModules) {
            if (CollectionUtils.isEmpty(module.getData())) {
              thisWorker.accept(
                  (AbstractFeaturedModule<AbstractModuleData>) module,
                  this::populateCollapsedModule);
            } else {
              thisPageData.setPrimaryMarketCache(
                  optimizeModule(thisPageData.getPrimaryMarketCache(), module));
              thisPageData.addModule(module);
            }
          }
        });
  }

  /**
   * For collapsed models, the data block is empty in page model. It should be sequentially
   * processed with populateModules() method.
   *
   * @return Void - this is the end of chain
   */
  protected final AbstractWorker<AbstractFeaturedModule<AbstractModuleData>, Void>
      populateCollapsedModule() {
    return and(
        "POPULATE_COLLAPSED_MODULE",
        (thisWorker, collapsedModule) -> {
          final PageCacheUpdate thisPageData = (PageCacheUpdate) thisWorker.getThisContext();
          // TODO: instead calling each collapsed module better have another REST call to call all
          // needed modules
          featuredMiddlewareContext
              .featuredService()
              .getModule(
                  collapsedModule.getId(),
                  String.valueOf(thisPageData.getPageVersion().getVersion()),
                  thisModule -> {
                    if (Objects.nonNull(thisModule)) {
                      // Event::Market cache creation.
                      thisPageData.setPrimaryMarketCache(
                          optimizeModule(thisPageData.getPrimaryMarketCache(), thisModule));
                      thisPageData.addModule(thisModule);
                    }
                    lockBetweenWorkers.countDown();
                  });
        });
  }

  @RootWorker
  public final AbstractWorker<String, PageRawIndex.GenerationKey> structureChanged(
      PageCacheUpdate thisPageData) {
    return and(
        thisPageData,
        (thisWorker, generationId) -> {
          log.info("Started a structure changed worker, generationId -> {}.", generationId);

          featuredMiddlewareContext
              .featuredService()
              .getFeaturedPagesStructure(
                  generationId,
                  featuredModel -> {
                    if (Objects.nonNull(featuredModel)) {
                      thisPageData.setPageModel(featuredModel);
                      thisWorker.accept(thisPageData.getPageVersion(), this::populateModules);

                      // Need to wait until all collapsed modules are processed
                      try {
                        boolean allWorkersDone =
                            lockBetweenWorkers.await(
                                FEATURED_COLLAPSED_MODULES_TIMEOUT, TimeUnit.SECONDS);
                        if (!allWorkersDone) {
                          log.warn(
                              "lockBetweenWorkers CountDownLatch waiting time elapsed before the count reached zero");
                        }
                      } catch (Exception e) {
                        log.error("structureChanged CountDownLatch exception {0}", e);
                      }
                      featuredMiddlewareContext.registerNewPageId(
                          PageRawIndex.fromGenerationKey(thisPageData.getPageVersion()));
                      featuredMiddlewareContext.applyWorkingCache(thisPageData);
                      clientCacheChangedNotifier(generationId).start(null);
                    }
                  });
        });
  }

  /** Requests modules for this featured model. */
  public void processLiveUpdate(String eventId, String payload) {
    try {
      // increments live updates counter.
      getContext().getFeaturedCachedData().getTicksMetrics().incLiveUpdatesTickCounter();
      BaseObject baseObject = objectMapper.readValue(payload, BaseObject.class);
      track(baseObject, eventId);
      sendToRoom(eventId, baseObject);

      // added payload for live updates cache.
      getContext().getFeaturedCachedData().addLiveUpdatesCache(baseObject);

      reflectLiveUpdates(baseObject.getEvent().getEventId().toString()).start(baseObject);
    } catch (Exception e) {
      log.error("While parsing", e);
      NewRelic.noticeError(e);
    }
  }

  // Can't use getRoomOperations(roomName).sendEvent(roomName, liveUpdate) because of bug
  // By iterating over room clients manually, we, effectively, overcome this
  // Can be changed once https://github.com/mrniko/netty-socketio/issues/677 is resolved
  private void sendToRoom(String roomName, BaseObject liveUpdate) {
    BroadcastOperations roomOperations = getContext().socketIOServer().getRoomOperations(roomName);
    Collection<SocketIOClient> clientsInRoom = roomOperations.getClients();
    clientsInRoom.forEach(client -> client.sendEvent(roomName, liveUpdate));
  }

  @Trace(dispatcher = true)
  private void track(BaseObject baseObject, String room) {
    NewRelic.setTransactionName(null, liveUpdateTransactionName + baseObject.getType());
    log.debug("[FeaturedChainFactory: liveUpdates ] room: {} -> {}", room, baseObject.hashCode());
  }

  @RootWorker
  public final AbstractWorker<BaseObject, FeaturedByEventMarket> reflectLiveUpdates(String lockId) {
    return and(
        lockId,
        (thisWorker, baseObject) -> {
          final Map<String, FeaturedByEventMarket> primaryMarketCache =
              featuredMiddlewareContext.getFeaturedCachedData().getPrimaryMarketCache();
          final String eventId = baseObject.getEvent().getEventId().toString();
          if (!primaryMarketCache.containsKey(eventId)) {
            log.info(
                "[ FeaturedFeaturedChainFactory:reflectLiveUpdates ] no event in primary market cache {}",
                eventId);
            return;
          }
          final FeaturedByEventMarket cachedEventByMarket = primaryMarketCache.get(eventId);
          final EventsModuleData event = cachedEventByMarket.getModuleData();

          switch (baseObject.getType()) {
            case "PRICE":
              final BaseObject.Outcome thisOutcome = baseObject.getEvent().getMarket().getOutcome();
              event.getMarkets().stream()
                  .map(OutputMarket::getOutcomes)
                  .flatMap(List::stream)
                  .filter(outcome -> outcome.isEqualsById(thisOutcome.getOutcomeId()))
                  .map(OutputOutcome::getPrices)
                  .flatMap(List::stream)
                  .forEach(
                      price -> {
                        price.setPriceDen(Integer.parseInt(thisOutcome.getPrice().getLpDen()));
                        price.setPriceNum(Integer.parseInt(thisOutcome.getPrice().getLpNum()));
                      });
              break;
            case "EVMKT":
              if (baseObject.getEvent().getMarket().getDisplayed().equals("N")
                  || baseObject.getEvent().getMarket().getStatus().equals("S")) {
                log.info(
                    "[ FeaturedFeaturedChainFactory:reflectLiveUpdates ] updating event in primary market cache {}",
                    eventId);
                if (applyPrimaryMarketLiveUpdate(
                    cachedEventByMarket,
                    baseObject.getEvent().getMarket().getMarketId().toString())) {
                  thisWorker.accept(
                      cachedEventByMarket,
                      () ->
                          raiseEventForModuleChanging(cachedEventByMarket.getModuleData().getId()));
                }
              }
              break;

            default:
          }
        });
  }

  public AbstractWorker<FeaturedByEventMarket, Void> raiseEventForModuleChanging(String eventId) {
    return and(
        eventId,
        (thisWorker, eventByMarket) ->
            eventByMarket
                .getModuleIds()
                .forEach(
                    moduleId ->
                        featuredMiddlewareContext
                            .getFeaturedCachedData()
                            .findModuleById(moduleId)
                            .ifPresent(
                                entity -> {
                                  BroadcastOperations roomOperations =
                                      featuredMiddlewareContext
                                          .socketIOServer()
                                          .getRoomOperations(moduleId);
                                  roomOperations.sendEvent(
                                      moduleId, minifyModule(entity.getValue()));
                                  log.info(
                                      "[ SportChainFactory:raiseEventForModuleChanging ] moduleId {}",
                                      moduleId);
                                })));
  }

  /**
   * Notify relation on FEATURED_STRUCTURE_CHANGED event.
   *
   * @param generationId model version -> [pageType::pageId::Version]
   * @return worker which can do this.
   */
  public AbstractWorker<Void, Void> clientCacheChangedNotifier(String generationId) {
    log.info("clientCacheChangedNotifier: {}", generationId);
    return and(
        generationId,
        (thisWorker, model) -> {
          PageRawIndex pageIndex = PageRawIndex.fromGenerationId(generationId);
          FeaturedModel featuredModel =
              featuredMiddlewareContext.getFeaturedCachedData().getStructure(pageIndex);

          SocketIOServer server = featuredMiddlewareContext.socketIOServer();
          BroadcastOperations roomOperationsUniversal =
              server.getRoomOperations(
                  pageIndex.getSportId() + HASH + FEATURED_STRUCTURE_CHANGED.messageId());
          if (featuredModel != null && featuredModel.isSegmented())
            addSegmentedModulesToChangeNotifier(featuredModel, server, roomOperationsUniversal);
          else {
            roomOperationsUniversal.sendEvent(
                FEATURED_STRUCTURE_CHANGED.messageId(), featuredModel);
          }
        });
  }

  private void addSegmentedModulesToChangeNotifier(
      FeaturedModel featuredModel,
      SocketIOServer server,
      BroadcastOperations roomOperationsUniversal) {
    List<AbstractFeaturedModule<?>> nonSegmentedModules = new ArrayList<>();
    SegmentedFeaturedModelHelper.fillNonSegmentedModules(featuredModel, nonSegmentedModules);
    if (featuredModel.getSegmentWiseModules() != null) {
      Map<String, SegmentView> segmentWiseModules = featuredModel.getSegmentWiseModules();
      segmentWiseModules
          .entrySet()
          .forEach(
              (Map.Entry<String, SegmentView> entry) -> {
                SegmentView segmentView = entry.getValue();
                SegmentedFeaturedModel segmentedFeaturedModel =
                    SegmentedFeaturedModelHelper.createSegmentedFeaturedModel(featuredModel);
                SegmentedFeaturedModelHelper.populateSegmentedFeaturedModel(
                    featuredModel, segmentedFeaturedModel, segmentView);
                segmentedFeaturedModel.addModules(nonSegmentedModules);
                if (UNIVERSAL_SEGMENT.equals(entry.getKey())) {
                  roomOperationsUniversal.sendEvent(
                      FEATURED_STRUCTURE_CHANGED.messageId(), segmentedFeaturedModel);
                  addClientsToModuleAndEventRooms(
                      entry.getKey(), segmentedFeaturedModel, roomOperationsUniversal, false);
                } else {
                  BroadcastOperations roomOperationsSegmented =
                      server.getRoomOperations(
                          featuredModel.getPageId()
                              + HASH
                              + entry.getKey()
                              + HASH
                              + FEATURED_STRUCTURE_CHANGED.messageId());
                  roomOperationsSegmented.sendEvent(
                      FEATURED_STRUCTURE_CHANGED.messageId(), segmentedFeaturedModel);
                  addClientsToModuleAndEventRooms(
                      entry.getKey(), segmentedFeaturedModel, roomOperationsSegmented, true);
                }
              });
    }
    if (featuredModel.getFanzoneSegmentWiseModules() != null) {
      addClientsToModuleAndEventRoomsForFanzone(featuredModel, server);
    }
  }
  /**
   * addClients to ModuleAndEventRooms for Fanzone
   *
   * @param featuredModel
   * @param server
   */
  private void addClientsToModuleAndEventRoomsForFanzone(
      FeaturedModel featuredModel, SocketIOServer server) {
    log.info("Started executing addClientsToModuleAndEventRoomsForFanzone");
    Map<String, FanzoneSegmentView> fanzoneSegmentViewMap =
        featuredModel.getFanzoneSegmentWiseModules();
    fanzoneSegmentViewMap
        .entrySet()
        .forEach(
            (Map.Entry<String, FanzoneSegmentView> entry) -> {
              FanzoneSegmentView fanzoneSegmentView = entry.getValue();
              SegmentedFeaturedModel segmentedFeaturedModel =
                  SegmentedFeaturedModelHelper.createSegmentedFeaturedModel(featuredModel);
              SegmentedFeaturedModelHelper.populateFanzoneSegmentedFeaturedModel(
                  featuredModel, segmentedFeaturedModel, fanzoneSegmentView, entry.getKey());
              BroadcastOperations roomOperationsSegmented =
                  server.getRoomOperations(
                      featuredModel.getPageId()
                          + HASH
                          + entry.getKey()
                          + HASH
                          + FEATURED_STRUCTURE_CHANGED.messageId());
              roomOperationsSegmented.sendEvent(
                  FEATURED_STRUCTURE_CHANGED.messageId(), segmentedFeaturedModel);
              addClientsToModuleAndEventRooms(
                  entry.getKey(), segmentedFeaturedModel, roomOperationsSegmented, true);
            });
    log.info("Ended executing addClientsToModuleAndEventRoomsForFanzone");
  }

  private void addClientsToModuleAndEventRooms(
      String segment,
      SegmentedFeaturedModel segmentedFeaturedModel,
      BroadcastOperations room,
      boolean isSegmented) {
    room.getClients().stream()
        .parallel()
        .forEach(
            client ->
                CompletableFuture.runAsync(
                    () -> {
                      SocketIoRoomSubscriber initVisitor =
                          new SocketIoRoomSubscriber(client, sportsSessionContext);
                      segmentedFeaturedModel.getModules().stream()
                          .forEach(
                              (AbstractFeaturedModule<?> m) -> {
                                if (isSegmented
                                    && (m instanceof SurfaceBetModule
                                        || m instanceof QuickLinkModule
                                        || m instanceof InplayModule)) {
                                  m.accept(initVisitor, segment);
                                } else {
                                  m.accept(initVisitor);
                                }
                              });
                    }));
  }

  /**
   * To create the chain of module processing for `FEATURED_MODULE_CONTENT_CHANGED_MINOR` event.
   *
   * <p>args[0] - (moduleId) new requested module id args[1] - (generationId) id of generation for
   * the module
   *
   * @return for made an updates for this module in cache structure and updates the subscriptions
   *     for depended topics.
   */
  @RootWorker()
  public AbstractWorker<String[], AbstractFeaturedModule<AbstractModuleData>>
      moduleContentMinorChanged() {
    final SportsCachedData thisCache = featuredMiddlewareContext.getFeaturedCachedData();
    return and(
        thisCache,
        (thisWorker, args) ->
            featuredMiddlewareContext
                .featuredService()
                .getModule(
                    args[0],
                    args[1],
                    module -> {
                      if (Objects.nonNull(module)) {
                        log.info(
                            "FeaturedChainFactory:moduleContentMinorChanged id->{}",
                            module.getId());
                        processModule(module, thisCache); // ---->
                      }
                    }));
  }

  /**
   * To create the chain of module processing for `FEATURED_MODULE_CONTENT_CHANGED` event.
   *
   * <p>args[0] - (moduleId) new requested module id args[1] - (generationId) id of generation for
   * the module
   *
   * @return for made an updates for this module in cache structure and updates the subscriptions
   *     for depended topics.
   */
  @RootWorker()
  public AbstractWorker<String[], AbstractFeaturedModule<AbstractModuleData>>
      moduleContentChanged() {
    final SportsCachedData thisCache = featuredMiddlewareContext.getFeaturedCachedData();
    return and(
        thisCache,
        (thisWorker, args) ->
            featuredMiddlewareContext
                .featuredService()
                .getModule(
                    args[0],
                    args[1],
                    module -> {
                      if (Objects.nonNull(module)) {
                        log.info(
                            "FeaturedChainFactory:moduleContentChanged id->{}", module.getId());
                        moduleContentChanged(thisCache, module);
                      }
                    }));
  }

  private void moduleContentChanged(SportsCachedData thisCache, AbstractFeaturedModule module) {

    processModule(module, thisCache);
    final SocketIOServer server = featuredMiddlewareContext.socketIOServer();

    if (module.isSegmented()) {
      // BMA-62181: updating on surfaceBet module on contentChanged.
      if (module instanceof SurfaceBetModule && module.getSportId().equals(FANZONE_PAGE_ID)) {
        fzSurfaceBetModule(server, ((SurfaceBetModule) module));
      } else if (module instanceof SurfaceBetModule) {
        surfaceBetModule(server, ((SurfaceBetModule) module));
      } else if (module instanceof QuickLinkModule) {
        if (module.getSportId().equals(FANZONE_PAGE_ID)) {
          fzQuickLinkModule(server, ((QuickLinkModule) module));
        } else {
          quickLinkModule(server, ((QuickLinkModule) module));
        }
      } else if (module instanceof InplayModule) {
        inPlayModule(server, ((InplayModule) module));
      } else if (module instanceof TeamBetsModule) {
        teamBetsModule(server, ((TeamBetsModule) module));
      } else if (module instanceof FanBetsModule) {
        fanBetsModule(server, ((FanBetsModule) module));
      } else {
        CompletableFuture.runAsync(() -> joinRoomForContentsInModule(module, server));
      }
    } else {
      BroadcastOperations rooms =
          server.getRoomOperations(module.getSportId() + HASH + module.getId());
      sendMessageToRoom(server, rooms, minifyModule(module));
    }
  }

  private void fzSurfaceBetModule(final SocketIOServer server, final SurfaceBetModule module) {
    module
        .getFanzoneModuleSegmentView()
        .forEach(
            (String k, FanzoneSegmentView v) -> {
              SurfaceBetModule surfaceBetModule =
                  (SurfaceBetModule)
                      ((EventsModule) module)
                          .copyWithEmptySegmentedData(module.getDisplayOrder().doubleValue());
              List<EventsModuleData> data =
                  v.getSurfaceBetModuleData().values().stream().collect(Collectors.toList());
              surfaceBetModule.setData(data);
              BroadcastOperations rooms =
                  server.getRoomOperations(
                      surfaceBetModule.getSportId() + HASH + k + HASH + surfaceBetModule.getId());
              sendMessageToRoom(server, rooms, minifyModule(surfaceBetModule));
            });
  }

  private void surfaceBetModule(final SocketIOServer server, final SurfaceBetModule module) {

    module
        .getModuleSegmentView()
        .forEach(
            (String k, SegmentView v) -> {
              SurfaceBetModule surfaceBetModule =
                  (SurfaceBetModule)
                      ((EventsModule) module)
                          .copyWithEmptySegmentedData(module.getDisplayOrder().doubleValue());
              List<EventsModuleData> data =
                  SegmentedFeaturedModelHelper.getSurfaceBetDataFromSegmentView(v);
              surfaceBetModule.setData(data);

              BroadcastOperations rooms =
                  getRooms(k, surfaceBetModule.getId(), server, surfaceBetModule.getSportId());
              sendMessageToRoom(server, rooms, minifyModule(surfaceBetModule));
            });
  }

  private void fzQuickLinkModule(final SocketIOServer server, final QuickLinkModule module) {
    module
        .getFanzoneModuleSegmentView()
        .forEach(
            (String k, FanzoneSegmentView v) -> {
              QuickLinkModule quickLinkModule =
                  module.copyWithEmptySegmentedData(module.getDisplayOrder().doubleValue());
              List<AbstractModuleData> data =
                  v.getQuickLinkModuleData().values().stream()
                      .map(
                          quickLinkData ->
                              SegmentedFeaturedModelHelper.cloneAbstractModuleData(
                                  quickLinkData, quickLinkData.getSegmentOrder()))
                      .filter(
                          abstractModuleData -> abstractModuleData.getFanzoneSegments().contains(k))
                      .collect(Collectors.toList());
              quickLinkModule.setData(data);
              BroadcastOperations rooms =
                  server.getRoomOperations(
                      quickLinkModule.getSportId() + HASH + k + HASH + quickLinkModule.getId());
              sendMessageToRoom(server, rooms, minifyModule(quickLinkModule));
            });
  }

  private void quickLinkModule(final SocketIOServer server, final QuickLinkModule module) {
    module
        .getModuleSegmentView()
        .forEach(
            (String k, SegmentView v) -> {
              QuickLinkModule quickLinkModule =
                  module.copyWithEmptySegmentedData(module.getDisplayOrder().doubleValue());
              List<AbstractModuleData> data =
                  SegmentedFeaturedModelHelper.getQuickLinkDataFromSegmentView(v);
              quickLinkModule.setData(data);
              BroadcastOperations rooms =
                  getRooms(k, quickLinkModule.getId(), server, quickLinkModule.getSportId());

              sendMessageToRoom(server, rooms, minifyModule(quickLinkModule));
            });
  }

  private void inPlayModule(final SocketIOServer server, final InplayModule module) {
    module
        .getModuleSegmentView()
        .forEach(
            (String k, SegmentView v) -> {
              InplayModule inplayModule =
                  module.copyWithEmptySegmentedData(module.getDisplayOrder().doubleValue());
              List<SportSegment> data =
                  SegmentedFeaturedModelHelper.getInplayModuleDataFromSegmentView(v);
              inplayModule.setData(data);
              BroadcastOperations rooms =
                  getRooms(k, inplayModule.getId(), server, inplayModule.getSportId());
              sendMessageToRoom(server, rooms, minifyModule(inplayModule));
            });
  }

  private void fanBetsModule(final SocketIOServer server, final FanBetsModule module) {
    if (module.getSportId().equals(FANZONE_PAGE_ID)) {
      module
          .getFanzoneModuleSegmentView()
          .forEach(
              (String k, FanzoneSegmentView v) -> {
                FanBetsModule fbmodule =
                    module.copyWithEmptySegmentedData(module.getDisplayOrder().doubleValue());
                List<FanBetsConfig> data =
                    v.getFanBetsModuleData().values().stream()
                        .map(
                            (FanBetsConfig t) -> {
                              t.setFanzoneSegments(null);
                              return t;
                            })
                        .collect(Collectors.toList());
                fbmodule.setData(data);

                BroadcastOperations rooms =
                    server.getRoomOperations(
                        fbmodule.getSportId() + HASH + k + HASH + fbmodule.getId());
                sendMessageToRoom(server, rooms, minifyModule(fbmodule));
              });
    }
  }

  private void teamBetsModule(final SocketIOServer server, final TeamBetsModule module) {
    if (module.getSportId().equals(FANZONE_PAGE_ID)) {
      module
          .getFanzoneModuleSegmentView()
          .forEach(
              (String k, FanzoneSegmentView v) -> {
                TeamBetsModule tbmodule =
                    module.copyWithEmptySegmentedData(module.getDisplayOrder().doubleValue());
                List<TeamBetsConfig> data =
                    v.getTeamBetsModuleData().values().stream()
                        .map(
                            (TeamBetsConfig t) -> {
                              t.setFanzoneSegments(null);
                              return t;
                            })
                        .collect(Collectors.toList());
                tbmodule.setData(data);

                BroadcastOperations rooms =
                    server.getRoomOperations(
                        tbmodule.getSportId() + HASH + k + HASH + tbmodule.getId());
                sendMessageToRoom(server, rooms, minifyModule(tbmodule));
              });
    }
  }

  private BroadcastOperations getRooms(
      String segment, String id, SocketIOServer server, final Integer sportId) {
    return UNIVERSAL_SEGMENT.equals(segment)
        ? server.getRoomOperations(sportId + HASH + id)
        : server.getRoomOperations(sportId + HASH + segment + HASH + id);
  }

  private void sendMessageToRoom(
      SocketIOServer server, BroadcastOperations rooms, AbstractFeaturedModule<?> module) {
    rooms.sendEvent(module.getId(), minifyModule(module));
    NewRelic.incrementCounter("moduleContentChanged-" + module.getSportId());
    NewRelic.incrementCounter("moduleContentChanged-" + module.getSportId() + "-" + module.getId());
    CompletableFuture.runAsync(() -> joinRoomForContentsInModule(module, server));
  }

  private void joinRoomForContentsInModule(
      AbstractFeaturedModule<?> module, SocketIOServer server) {
    if (ModuleType.FEATURED.equals(module.getModuleType())) {
      EventsModule eventModule = (EventsModule) module;
      if (eventModule.getData() != null) {
        server.getAllClients().forEach(cl -> joinEventRoomIfNotJoined(cl, eventModule));
      }
    }
  }

  private void joinEventRoomIfNotJoined(SocketIOClient client, EventsModule eventModule) {
    Set<String> eventsIds =
        eventModule.getData().stream()
            .map(EventsModuleData::getId)
            .map(String::valueOf)
            .collect(Collectors.toSet());
    Set<String> clientRooms = client.getAllRooms();
    eventsIds.stream().filter(room -> !clientRooms.contains(room)).forEach(client::joinRoom);
  }

  public AbstractWorker<PageRawIndex, FeaturedModel> addSportPage(String generationId) {
    return and(
        generationId,
        (thisWorker, pageIndex) -> featuredMiddlewareContext.registerNewPageId(pageIndex));
  }

  public AbstractWorker<PageRawIndex, FeaturedModel> deleteSportPage(String generationId) {
    return and(
        generationId,
        (thisWorker, rmPageIndex) -> {
          FeaturedModel thisPage =
              featuredMiddlewareContext.getFeaturedCachedData().getStructure(rmPageIndex);
          if (thisPage == null) {
            log.warn("SportChainFactory:deleteSportPage nothing to delete. {}", rmPageIndex);
            return;
          }
          PageCacheUpdate rmUpdate =
              PageCacheUpdate.builder()
                  .pageVersion(PageRawIndex.GenerationKey.fromString(generationId))
                  .pageModel(
                      FeaturedModel.builder()
                          .pageId(thisPage.getPageId())
                          .title(thisPage.getTitle())
                          .showTabOn(thisPage.getShowTabOn())
                          .visible(thisPage.isVisible())
                          .directiveName(thisPage.getDirectiveName())
                          .useFSCCached(thisPage.isUseFSCCached())
                          .build())
                  .build();
          featuredMiddlewareContext.applyWorkingCache(rmUpdate);
          featuredMiddlewareContext.removePageIdFromCache(String.valueOf(rmPageIndex.getSportId()));
          thisWorker.accept(rmUpdate.getPageModel(), this::clientStructureChangeNotifier);
        });
  }

  public AbstractWorker<FeaturedModel, Void> clientStructureChangeNotifier() {
    return and(
        "CLIENT_STRUCTURE_CHANGE_NOTIFIER",
        (thisWorker, pageModel) -> {
          BroadcastOperations roomOperations =
              featuredMiddlewareContext
                  .socketIOServer()
                  .getRoomOperations(
                      PageRawIndex.fromModel(pageModel).getSportId()
                          + HASH
                          + FEATURED_STRUCTURE_CHANGED.messageId());
          roomOperations.sendEvent(FEATURED_STRUCTURE_CHANGED.messageId(), pageModel);
        });
  }

  /**
   * To create workers chain with a full flow of processes which can update the cache in middleware
   * context and subscribe on necessary topics.
   *
   * @return the first worker from the chain.
   */
  @Override
  @RootWorker()
  public AbstractWorker getScheduledJob() {
    return workerVersion();
  }

  @Override
  public DiagnosticService diagnosticService() {
    return diagnosticService;
  }
}
