package com.coral.oxygen.middleware.featured.configuration;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.middleware.common.service.AssetManagementService;
import com.coral.oxygen.middleware.common.service.featured.OddsCardHeader;
import com.coral.oxygen.middleware.featured.consumer.FeaturedDataConsumer;
import com.coral.oxygen.middleware.featured.consumer.sportpage.*;
import com.coral.oxygen.middleware.featured.consumer.sportpage.bets.PopularBetModuleProcessor;
import com.coral.oxygen.middleware.featured.consumer.sportpage.virtual.VirtualEventsModuleProcessor;
import com.coral.oxygen.middleware.featured.service.*;
import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector;
import com.coral.oxygen.middleware.featured.service.injector.FeaturedCommentaryInjector;
import com.coral.oxygen.middleware.featured.service.injector.MarketsCountInjector;
import com.coral.oxygen.middleware.featured.service.injector.RacingEventsModuleInjector;
import com.coral.oxygen.middleware.featured.service.injector.SingleOutcomeEventsModuleInjector;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Data
@Configuration
@RequiredArgsConstructor
@ConditionalOnProperty(name = "featured.scheduled.task.enabled")
public class FeaturedConfiguration {
  private final EventDataInjector eventDataInjector;
  private final SingleOutcomeEventsModuleInjector singleOutcomeDataInjector;
  private final RacingEventsModuleInjector racingDataInjector;
  private final MarketsCountInjector marketsCountInjector;
  private final FeaturedCommentaryInjector commentaryInjector;
  private final FeaturedDataFilter featuredDataFilter;
  private final OddsCardHeader oddsCardHeader;
  private final BybService bybService;
  private final CmsService cmsService;
  private final HighlightCarouselModuleProcessor highlightCarouselModuleProcessor;
  private final FanzoneHighlightCarouselModuleProcessor fanzonehighlightCarouselModuleProcessor;
  private final SportPageFilter sportPageFilter;
  private final SurfaceBetModuleProcessor surfaceBetModuleProcessor;
  private final FanzoneSurfaceBetModuleProcessor fanzoneSurfaceBetModuleProcessor;
  private final InplayModuleConsumer inplayModuleConsumer;
  private final FeaturedModuleProcessor featuredModuleProcessor;
  private final AemCarouselsProcessor aemCarouselsProcessor;
  private final QuickLinkModuleProcessor quickLinkModuleProcessor;
  private final FanzoneQuickLinkModuleProcessor fanzoneQuickLinkModuleProcessor;
  private final RacingModuleProcessor racingModuleProcessor;
  private final FeaturedModelStorageService storageService;
  private final AssetManagementService assetManagementService;
  private final FeaturedNextRacesConfigProcessor nextRacesConfigProcessor;
  private final TeamBetsFZModuleProcessor teamBetsFZModuleProcessor;
  private final FanBetsFZModuleProcessor fanBetsFZModuleProcessor;
  private final VirtualEventsModuleProcessor virtualEventsModuleProcessor;
  private final PopularBetModuleProcessor popularBetModuleProcessor;
  private final BybWidgetProcessor bybWidgetProcessor;
  private final LuckyDipModuleProcessor luckyDipModuleProcessor;
  private final PopularAccaModuleProcessor popularAccaModuleProcessor;

  @Bean
  public FeaturedDataConsumer createFeaturedDataConsumer() {
    return new FeaturedDataConsumer(this);
  }
}
