package com.oxygen.publisher.sportsfeatured.service;

import com.oxygen.publisher.sportsfeatured.context.SportsMiddlewareContext;
import com.oxygen.publisher.sportsfeatured.model.FeaturedByEventMarket;
import com.oxygen.publisher.sportsfeatured.model.FeaturedModel;
import com.oxygen.publisher.sportsfeatured.model.Identifier;
import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.module.*;
import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData;
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.SportSegment;
import java.util.*;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;

/**
 * yet another abstraction, which purpose is to reduce {@link AbstractSportsChainFactory} & contain
 * {@link com.oxygen.publisher.sportsfeatured.model.module.AbstractFeaturedModule} module related
 * operations
 */
@Slf4j
public abstract class AbstractModuleFactory {

  protected abstract SportsMiddlewareContext getContext();

  /**
   * Method lookups through {@link FeaturedModel} list of modules for one with the same id &
   * replaces it entirely
   */
  protected <T extends AbstractFeaturedModule<?>> void fixOldModule(
      T module, FeaturedModel structure) {
    Identifier moduleIdentifier = module.getIdentifier();
    List<T> structureModules = structure.getModules(moduleIdentifier);
    if (!CollectionUtils.isEmpty(structureModules)) {
      structureModules.stream()
          .filter(module::isEqualsById)
          .findFirst()
          .filter(AbstractFeaturedModule::hasData)
          .ifPresent(
              eventsModuleToReplace ->
                  structure.replaceModules(moduleIdentifier, Collections.singletonList(module)));
      log.info("Updated Featured structure because of expanded module {} update.", module.getId());
    }
  }

  protected <T extends AbstractFeaturedModule<?>> void updateModuleInSegmentWiseModules(
      T module, FeaturedModel structure) {
    Map<String, SegmentView> segmentWiseModules = structure.getSegmentWiseModules();
    if (module.getSegments() != null
        && (module instanceof EventsModule
            || module instanceof QuickLinkModule
            || module instanceof InplayModule)) {
      module
          .getSegments()
          .forEach(
              (String segment) -> {
                SegmentView segView = segmentWiseModules.get(segment);
                if (segView != null) {
                  if (module instanceof HighlightCarouselModule) {
                    segView
                        .getHighlightCarouselModules()
                        .put(
                            module.getId(),
                            module
                                .getModuleSegmentView()
                                .get(segment)
                                .getHighlightCarouselModules()
                                .get(module.getId()));
                  } else if (module instanceof SurfaceBetModule surfaceBetModule) {
                    structure.setSurfaceBetModule(surfaceBetModule);
                    module
                        .getModuleSegmentView()
                        .get(segment)
                        .getSurfaceBetModuleData()
                        .entrySet()
                        .forEach(
                            entry ->
                                segView
                                    .getSurfaceBetModuleData()
                                    .put(entry.getKey(), entry.getValue()));
                  } else if (module instanceof EventsModule) {
                    segView
                        .getEventModules()
                        .put(
                            module.getId(),
                            module
                                .getModuleSegmentView()
                                .get(segment)
                                .getEventModules()
                                .get(module.getId()));
                  } else if (module instanceof QuickLinkModule quickLinkModule) {
                    structure.setQuickLinkModule(quickLinkModule);
                    module
                        .getModuleSegmentView()
                        .get(segment)
                        .getQuickLinkData()
                        .entrySet()
                        .forEach(
                            entry ->
                                segView.getQuickLinkData().put(entry.getKey(), entry.getValue()));
                  } else {
                    structure.setInplayModule((InplayModule) module);
                    module
                        .getModuleSegmentView()
                        .get(segment)
                        .getInplayModuleData()
                        .entrySet()
                        .forEach(
                            entry ->
                                segView
                                    .getInplayModuleData()
                                    .put(entry.getKey(), entry.getValue()));
                  }
                }
              });
    }
  }
  /**
   * Fanzone BMA-62182 updating Module in FanzoneSegmentWiseModules
   *
   * @param module
   * @param structure
   * @param <T>
   */
  protected <T extends AbstractFeaturedModule<?>> void updateModuleInFanzoneSegmentWiseModules(
      T module, FeaturedModel structure) {
    Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules =
        structure.getFanzoneSegmentWiseModules();
    if (module.getFanzoneSegments() != null) {
      module
          .getFanzoneSegments()
          .forEach(
              (String segment) -> {
                FanzoneSegmentView fzSegView = fanzoneSegmentWiseModules.get(segment);
                if (fzSegView != null) {
                  if (module instanceof HighlightCarouselModule) {
                    fzSegView
                        .getHighlightCarouselModules()
                        .put(
                            module.getId(),
                            module
                                .getFanzoneModuleSegmentView()
                                .get(segment)
                                .getHighlightCarouselModules()
                                .get(module.getId()));
                  } else if (module instanceof SurfaceBetModule surfaceBetModule) {
                    structure.setSurfaceBetModule(surfaceBetModule);
                    module
                        .getFanzoneModuleSegmentView()
                        .get(segment)
                        .getSurfaceBetModuleData()
                        .entrySet()
                        .forEach(
                            entry ->
                                fzSegView
                                    .getSurfaceBetModuleData()
                                    .put(entry.getKey(), entry.getValue()));
                  } else if (module instanceof QuickLinkModule quickLinkModule) {
                    structure.setQuickLinkModule(quickLinkModule);
                    module
                        .getFanzoneModuleSegmentView()
                        .get(segment)
                        .getQuickLinkModuleData()
                        .entrySet()
                        .forEach(
                            entry ->
                                fzSegView
                                    .getQuickLinkModuleData()
                                    .put(entry.getKey(), entry.getValue()));
                  } else if (module instanceof TeamBetsModule teamBetsModule) {
                    structure.setTeamBetsModule(teamBetsModule);
                    module
                        .getFanzoneModuleSegmentView()
                        .get(segment)
                        .getTeamBetsModuleData()
                        .entrySet()
                        .forEach(
                            entry ->
                                fzSegView
                                    .getTeamBetsModuleData()
                                    .put(entry.getKey(), entry.getValue()));

                  } else if (module instanceof FanBetsModule fanBetsModule) {

                    structure.setFanBetsModule(fanBetsModule);
                    module
                        .getFanzoneModuleSegmentView()
                        .get(segment)
                        .getFanBetsModuleData()
                        .entrySet()
                        .forEach(
                            entry ->
                                fzSegView
                                    .getFanBetsModuleData()
                                    .put(entry.getKey(), entry.getValue()));
                  }
                }
              });
    }
  }

  protected Map<String, FeaturedByEventMarket> optimizeEventsModule(
      Map<String, FeaturedByEventMarket> prMarketsCache, EventsModule module) {
    List<EventsModuleData> refModuleData = new ArrayList<>();
    module
        .getData()
        .forEach(
            moduleData -> {
              FeaturedByEventMarket thisEvent =
                  performCacheUpdateOperations(moduleData, prMarketsCache);

              thisEvent.getModuleIds().add(module.getId());
              refModuleData.add(thisEvent.getModuleData());
            });
    module.setData(refModuleData);
    return prMarketsCache;
  }

  protected Map<String, FeaturedByEventMarket> optimizeInplayModule(
      Map<String, FeaturedByEventMarket> prMarketsCache, InplayModule module) {
    module.getData().stream()
        .map(SportSegment::getEventsByTypeName)
        .flatMap(Collection::stream)
        .forEach(
            typeSegment -> {
              List<EventsModuleData> refModuleData = new ArrayList<>();
              typeSegment
                  .getEvents()
                  .forEach(
                      moduleData -> {
                        FeaturedByEventMarket thisEvent =
                            performCacheUpdateOperations(moduleData, prMarketsCache);
                        thisEvent.getModuleIds().add(module.getId());
                        refModuleData.add(thisEvent.getModuleData());
                      });
              typeSegment.setEvents(refModuleData);
            });

    return prMarketsCache;
  }

  private FeaturedByEventMarket performCacheUpdateOperations(
      EventsModuleData moduleData, Map<String, FeaturedByEventMarket> prMarketsCache) {
    String index = createPRMarketCacheIndex(moduleData);
    return !prMarketsCache.containsKey(index)
        ? createPrMarketCacheEntity(moduleData, prMarketsCache, index)
        : getPrMarketCacheEntity(moduleData, prMarketsCache, index);
  }

  private FeaturedByEventMarket getPrMarketCacheEntity(
      EventsModuleData moduleData,
      Map<String, FeaturedByEventMarket> prMarketsCache,
      String index) {
    FeaturedByEventMarket thisEvent;
    thisEvent = prMarketsCache.get(index);
    thisEvent.setModuleData(moduleData);
    thisEvent.setPrimaryMarkets(moduleData.getPrimaryMarkets());
    log.info(
        "[ AbstractFeaturedChainFactory:optimizeModule ] Replaced {} event from primary markets cache with "
            + "new version, market id {}. Primary markets number {}.",
        moduleData.getId(),
        CollectionUtils.isEmpty(moduleData.getMarkets())
            ? null
            : moduleData.getMarkets().get(0).getId(),
        moduleData.getPrimaryMarkets() == null ? null : moduleData.getPrimaryMarkets().size());
    return thisEvent;
  }

  private FeaturedByEventMarket createPrMarketCacheEntity(
      EventsModuleData moduleData,
      Map<String, FeaturedByEventMarket> prMarketsCache,
      String index) {
    FeaturedByEventMarket thisEvent;
    thisEvent =
        FeaturedByEventMarket.builder()
            .moduleData(moduleData)
            .primaryMarkets(moduleData.getPrimaryMarkets())
            .build();
    prMarketsCache.put(index, thisEvent);
    log.info(
        "[ AbstractFeaturedChainFactory:optimizeModule ] Put {} event into primary markets cache, "
            + "market id {}. Primary markets number {}.",
        moduleData.getId(),
        CollectionUtils.isEmpty(moduleData.getMarkets())
            ? null
            : moduleData.getMarkets().get(0).getId(),
        moduleData.getPrimaryMarkets() == null ? null : moduleData.getPrimaryMarkets().size());
    return thisEvent;
  }

  private String createPRMarketCacheIndex(EventsModuleData moduleData) {
    return moduleData.getId();
  }

  /** cut unnecessary fields from module for UI */
  protected AbstractFeaturedModule minifyModule(AbstractFeaturedModule module) {
    if (ModuleType.IN_PLAY.equals(module.getModuleType())) {
      return getMinifiedInPlayModule((InplayModule) module);
    } else {
      return module;
    }
  }

  private InplayModule getMinifiedInPlayModule(InplayModule module) {
    InplayModule inplayModule = new InplayModule();
    inplayModule.setId(module.getId());
    inplayModule.setSportId(module.getSportId());
    inplayModule.setTotalEvents(module.getTotalEvents());
    return inplayModule;
  }
}
