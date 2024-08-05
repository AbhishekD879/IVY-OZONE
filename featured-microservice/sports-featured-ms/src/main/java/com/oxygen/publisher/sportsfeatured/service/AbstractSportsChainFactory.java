package com.oxygen.publisher.sportsfeatured.service;

import com.newrelic.api.agent.NewRelic;
import com.oxygen.publisher.model.OutputMarket;
import com.oxygen.publisher.sportsfeatured.model.FeaturedByEventMarket;
import com.oxygen.publisher.sportsfeatured.model.FeaturedModel;
import com.oxygen.publisher.sportsfeatured.model.ModuleRawIndex;
import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex;
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import com.oxygen.publisher.sportsfeatured.model.module.*;
import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData;
import com.oxygen.publisher.translator.ChainFactory;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;

/** Created by Aliaksei Yarotski on 4/19/18. */
@Slf4j
public abstract class AbstractSportsChainFactory extends AbstractModuleFactory
    implements ChainFactory {

  /** list of modules, that currently support structure updates */
  protected static final List<ModuleType> SUPPORTED_MODULES =
      Collections.unmodifiableList(
          Arrays.asList(
              ModuleType.FEATURED,
              ModuleType.HIGHLIGHTS_CAROUSEL,
              ModuleType.VIRTUAL_NEXT_EVENTS,
              ModuleType.POPULAR_BETS,
              ModuleType.IN_PLAY,
              ModuleType.SURFACE_BET,
              ModuleType.BYB_WIDGET));

  /**
   * Method takes provided module, than looks up through primary markets cache (map of [eventId,
   * event]) for events contained in that module & creates/updates entries in cache.
   *
   * <p>NOTE: module contents are also modified
   */
  protected Map<String, FeaturedByEventMarket> optimizeModule(
      Map<String, FeaturedByEventMarket> prMarketsCache, AbstractFeaturedModule module) {
    if (Objects.isNull(module) || !SUPPORTED_MODULES.contains(module.getModuleType())) {
      log.info(
          "[optimizeEventsModule] {} Module cannot be processed since it's type {} is not supported yet",
          module.getTitle(),
          module.getModuleType());
      return prMarketsCache;
    }

    Map<String, FeaturedByEventMarket> result = null;
    switch (module.getModuleType()) {
      case IN_PLAY:
        result = optimizeInplayModule(prMarketsCache, (InplayModule) module);
        break;
      case FEATURED,
          HIGHLIGHTS_CAROUSEL,
          VIRTUAL_NEXT_EVENTS,
          SURFACE_BET,
          POPULAR_BETS,
          BYB_WIDGET:
      default:
        result = optimizeEventsModule(prMarketsCache, (EventsModule) module);
        break;
    }
    if (Objects.isNull(result)) {
      log.warn(
          "[optimizeModule] found no optimization handler for module type {} ",
          module.getModuleType());
    }
    return result;
  }

  protected final boolean applyPrimaryMarketLiveUpdate(
      FeaturedByEventMarket cachedEventByMarket, String removedMarketId) {
    if (cachedEventByMarket.getPrimaryMarkets() == null
        || cachedEventByMarket.getPrimaryMarkets().isEmpty()) {
      String errorMessage =
          String.format(
              "[ AbstractFeaturedChainFactory:applyPrimaryMarketLiveUpdate ]"
                  + " the primary markets collection is empty! Removed market id->%s",
              removedMarketId);
      log.error(errorMessage);
      NewRelic.noticeError(errorMessage);
      return false;
    }
    EventsModuleData thisEvent = cachedEventByMarket.getModuleData();
    if (CollectionUtils.isEmpty(thisEvent.getMarkets())) {
      String errorMessage =
          String.format(
              "[ AbstractFeaturedChainFactory:applyPrimaryMarketLiveUpdate ]"
                  + " the markets collection is empty for event id->%s!",
              thisEvent.getId());
      log.error(errorMessage);
      NewRelic.noticeError(errorMessage);
      return false;
    }
    OutputMarket oldMarket = thisEvent.getMarkets().get(0);
    if (!cachedEventByMarket.getPrimaryMarkets().contains(oldMarket)) {
      String errorMessage =
          String.format(
              "[ AbstractFeaturedChainFactory:applyPrimaryMarketLiveUpdate ] %s->%s "
                  + "not found in the primary market collection. ",
              thisEvent.getId(), oldMarket.getId());
      log.error(errorMessage);
      NewRelic.noticeError(errorMessage);
      return false;
    }

    List<OutputMarket> activePrimaryMarkets =
        cachedEventByMarket.getPrimaryMarkets().stream()
            .filter(outputMarket -> !outputMarket.getId().equals(removedMarketId))
            .collect(Collectors.toList());
    log.info(
        "[ AbstractFeaturedChainFactory:applyPrimaryMarketLiveUpdate ] {}->{} removed {} "
            + "from active primary markets list.",
        thisEvent.getId(),
        oldMarket.getId(),
        removedMarketId);
    cachedEventByMarket.setPrimaryMarkets(activePrimaryMarkets);
    if (oldMarket.getId().equals(removedMarketId)) {
      if (activePrimaryMarkets.isEmpty()) {
        log.info(
            "[ AbstractFeaturedChainFactory:applyPrimaryMarketLiveUpdate ] {}->{} removed the last primary market.",
            thisEvent.getId(),
            oldMarket.getId());
        thisEvent.setMarkets(Collections.emptyList());
      } else {
        log.info(
            "[ AbstractFeaturedChainFactory:applyPrimaryMarketLiveUpdate ] {}->{} set as market"
                + " next primary market {}.",
            thisEvent.getId(),
            oldMarket.getId(),
            activePrimaryMarkets.get(0).getId());
        thisEvent.getMarkets().set(0, activePrimaryMarkets.get(0));
      }
      return true;
    }
    return false;
  }

  /**
   * purpose of this method is to find modules with same id in cache & replace them with provided
   * one
   */
  protected <T extends AbstractFeaturedModule<?>> void processModule(
      T module, SportsCachedData thisCache) {
    PageRawIndex index = PageRawIndex.from(module.getSportId(), module.getPageType());
    FeaturedModel structure = getContext().getFeaturedCachedData().getStructure(index);
    if (isSegmented(structure)) {
      updateModuleInSegmentWiseModules(module, structure);
      updateModuleInFanzoneSegmentWiseModules(module, structure); // Fanzone BMA-62182
    }
    if (module instanceof QuickLinkModule) {
      updateQuickLinkCache((QuickLinkModule) module, thisCache);
      return;
    }

    if (module instanceof RecentlyPlayedGameModule) {
      updateRPGCache((RecentlyPlayedGameModule) module, thisCache);
      return;
    }

    if (module instanceof RacingModule) {
      updateRacingModuleCache((RacingModule) module, thisCache);
      return;
    }

    if (module instanceof AemBannersModule) {
      updateAemBanners((AemBannersModule) module, thisCache);
    }

    if (module instanceof LuckyDipModule luckyDipModule) {
      updateLuckyDip(luckyDipModule, thisCache);
    }

    if (checkForVirtualEventOrPopularBet(module, thisCache)) return;

    handleTeamBetsModule(module, thisCache);
    handleFanBetsModule(module, thisCache);

    if (!SUPPORTED_MODULES.contains(module.getModuleType())) {
      log.info(
          "[processModule] {} Module cannot be processed since it's type {} is not supported yet",
          module.getTitle(),
          module.getModuleType());
      return;
    }

    thisCache.updateModule(ModuleRawIndex.fromModule(module), module);

    if (structure != null) {
      fixOldModule(module, structure);
    } else {
      log.warn("Detected null Structure. Context: {}", getContext().getFeaturedCachedData());
    }
  }

  private <T extends AbstractFeaturedModule<?>> boolean checkForVirtualEventOrPopularBet(
      T module, SportsCachedData thisCache) {
    boolean flag = false;
    if (module instanceof VirtualEventModule m) {
      updateVirtualEventModuleCache(m, thisCache);
      flag = true;
    } else if (module instanceof PopularBetModule popularBetModule) {
      updatePopularBetModule(popularBetModule, thisCache);
      flag = true;
    }
    return flag;
  }

  private static boolean isSegmented(FeaturedModel structure) {
    return structure != null && structure.isSegmented();
  }

  private <T extends AbstractFeaturedModule<?>> void handleTeamBetsModule(
      T module, SportsCachedData thisCache) {
    if (module instanceof TeamBetsModule teambetsmodule) {
      updateTeamBetsCache(teambetsmodule, thisCache);
    }
  }

  private <T extends AbstractFeaturedModule<?>> void handleFanBetsModule(
      T module, SportsCachedData thisCache) {
    if (module instanceof FanBetsModule fanBetsModule) {
      updateFanBetsCache(fanBetsModule, thisCache);
    }
  }

  // Updates(replaces) thisCache and structure cache with new quicklink if matched by id
  private void updateQuickLinkCache(QuickLinkModule module, SportsCachedData thisCache) {
    thisCache.updateModule(ModuleRawIndex.fromModule(module), module);
    updateStructure(module);
  }

  // Updates(replaces) thisCache and structure cache with new RpgModule if matched by id
  private void updateRPGCache(RecentlyPlayedGameModule newRPGModule, SportsCachedData thisCache) {
    thisCache.updateModule(ModuleRawIndex.fromModule(newRPGModule), newRPGModule);
    updateStructure(newRPGModule);
  }

  private void updateVirtualEventModuleCache(
      VirtualEventModule virtualEventModule, SportsCachedData thisCache) {
    thisCache.updateModule(ModuleRawIndex.fromModule(virtualEventModule), virtualEventModule);
    updateStructure(virtualEventModule);
  }

  private void updatePopularBetModule(
      PopularBetModule popularBetModule, SportsCachedData thisCache) {
    thisCache.updateModule(ModuleRawIndex.fromModule(popularBetModule), popularBetModule);
    updateStructure(popularBetModule);
  }

  private void updateRacingModuleCache(RacingModule racingModule, SportsCachedData thisCache) {
    thisCache.updateModule(ModuleRawIndex.fromModule(racingModule), racingModule);
    updateStructure(racingModule);
  }

  private void updateAemBanners(AemBannersModule newBanners, SportsCachedData thisCache) {
    thisCache.updateModule(ModuleRawIndex.fromModule(newBanners), newBanners);
    updateStructure(newBanners);
  }

  private void updateTeamBetsCache(TeamBetsModule module, SportsCachedData thisCache) {
    thisCache.updateModule(ModuleRawIndex.fromModule(module), module);
    updateStructure(module);
  }

  private void updateFanBetsCache(FanBetsModule module, SportsCachedData thisCache) {
    thisCache.updateModule(ModuleRawIndex.fromModule(module), module);
    updateStructure(module);
  }

  private void updateLuckyDip(LuckyDipModule luckyDipModule, SportsCachedData thisCache) {
    thisCache.updateModule(ModuleRawIndex.fromModule(luckyDipModule), luckyDipModule);
    updateStructure(luckyDipModule);
  }

  private <T extends AbstractFeaturedModule<?>> void updateStructure(T newModule) {
    FeaturedModel structure =
        getContext()
            .getFeaturedCachedData()
            .getStructure(PageRawIndex.forSport(newModule.getSportId()));

    if (structure != null) {
      structure.replaceModules(newModule.getIdentifier(), Collections.singletonList(newModule));
    }
  }
}
