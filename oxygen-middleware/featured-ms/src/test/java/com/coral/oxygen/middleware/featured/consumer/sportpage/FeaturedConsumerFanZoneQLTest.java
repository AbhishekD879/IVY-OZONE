package com.coral.oxygen.middleware.featured.consumer.sportpage;

import static org.mockito.ArgumentMatchers.any;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.cms.api.SystemConfigProvider;
import com.coral.oxygen.middleware.common.configuration.CmsConfiguration;
import com.coral.oxygen.middleware.common.configuration.GsonConfiguration;
import com.coral.oxygen.middleware.common.configuration.MappersConfiguration;
import com.coral.oxygen.middleware.common.configuration.OkHttpClientCreator;
import com.coral.oxygen.middleware.common.configuration.SiteServerAPIConfiguration;
import com.coral.oxygen.middleware.common.service.AssetManagementService;
import com.coral.oxygen.middleware.common.service.DateTimeHelper;
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.coral.oxygen.middleware.common.service.SportsConfig;
import com.coral.oxygen.middleware.common.service.featured.OddsCardHeader;
import com.coral.oxygen.middleware.common.utils.OrdinalToNumberConverter;
import com.coral.oxygen.middleware.common.utils.QueryFilterBuilder;
import com.coral.oxygen.middleware.featured.aem.AemMetaConsumer;
import com.coral.oxygen.middleware.featured.configuration.FeaturedConfiguration;
import com.coral.oxygen.middleware.featured.consumer.FeaturedDataConsumer;
import com.coral.oxygen.middleware.featured.consumer.sportpage.bets.PopularBetModuleProcessor;
import com.coral.oxygen.middleware.featured.consumer.sportpage.virtual.VirtualEventsModuleProcessor;
import com.coral.oxygen.middleware.featured.service.*;
import com.coral.oxygen.middleware.featured.service.impl.PopularBetApi;
import com.coral.oxygen.middleware.featured.service.injector.DFRacingEventsModuleInjector;
import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector;
import com.coral.oxygen.middleware.featured.service.injector.FeaturedCommentaryInjector;
import com.coral.oxygen.middleware.featured.service.injector.MarketsCountInjector;
import com.coral.oxygen.middleware.featured.service.injector.RacingEventsModuleInjector;
import com.coral.oxygen.middleware.featured.service.injector.SingleOutcomeEventsModuleInjector;
import com.coral.oxygen.middleware.featured.utils.TestUtils;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModelsData;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex;
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest(
    classes = {
      CmsConfiguration.class,
      SiteServerAPIConfiguration.class,
      EventDataInjector.class,
      SingleOutcomeEventsModuleInjector.class,
      RacingEventsModuleInjector.class,
      MarketsCountInjector.class,
      FeaturedCommentaryInjector.class,
      MappersConfiguration.class,
      SportsConfig.class,
      GsonConfiguration.class,
      OrdinalToNumberConverter.class,
      FeaturedConfiguration.class,
      HighlightCarouselModuleProcessor.class,
      FanzoneHighlightCarouselModuleProcessor.class,
      SurfaceBetModuleProcessor.class,
      FanzoneSurfaceBetModuleProcessor.class,
      OkHttpClientCreator.class,
      FeaturedModuleProcessor.class,
      MarketTemplateNameService.class,
      FanzoneQuickLinkModuleProcessor.class,
      QuickLinkModuleProcessor.class,
      RecentlyPlayedGameModuleProcessor.class,
      DFRacingEventsModuleInjector.class,
      AemCarouselsProcessor.class,
      RacingModuleProcessor.class,
      DateTimeHelper.class,
      QueryFilterBuilder.class,
      FeaturedModelStorageService.class,
      MarketsCountInjector.class,
      TeamBetsFZModuleProcessor.class,
      FanBetsFZModuleProcessor.class,
      VirtualEventsModuleProcessor.class,
      PopularBetModuleProcessor.class,
      PopularBetApi.class,
      BybWidgetProcessor.class,
      LuckyDipModuleProcessor.class
    })
public class FeaturedConsumerFanZoneQLTest {
  @MockBean CmsService cmsService;
  @MockBean SiteServerApi siteServerApi;

  @MockBean PopularBetApi popularBetApi;

  @Autowired EventDataInjector eventDataInjector;
  @Autowired DateTimeHelper dateTimeHelper;
  @Autowired SingleOutcomeEventsModuleInjector singleOutcomeDataInjector;
  @MockBean RacingEventsModuleInjector racingDataInjector;
  @MockBean DFRacingEventsModuleInjector dfRacingEventsModuleInjector;
  @MockBean FeaturedCommentaryInjector commentaryInjector;
  @MockBean FeaturedDataFilter featuredDataFilter;
  @MockBean OddsCardHeader oddsCardHeader;
  @MockBean private BybService bybService;
  @MockBean private InplayModuleConsumer inplayModuleConsumer;
  @MockBean SportPageFilter sportPageFilter;
  @Autowired FeaturedDataConsumer featuredDataConsumer;
  @MockBean AemMetaConsumer aemMetaConsumer;
  @MockBean AemCarouselsProcessor aemCarouselsProcessor;
  @MockBean SystemConfigProvider systemConfigProvider;
  @MockBean RacingModuleProcessor racingModuleProcessor;
  @MockBean FeaturedModelStorageService storageService;
  @MockBean AssetManagementService assetManagementService;

  @MockBean VirtualEventsModuleProcessor virtualEventsModuleProcessor;
  @MockBean BybWidgetProcessor bybWidgetProcessor;

  @MockBean FeaturedNextRacesConfigProcessor featuredNextRacesConfigProcessor;

  @MockBean PopularBetModuleProcessor popularBetModuleProcessor;
  @MockBean LuckyDipModuleProcessor luckyDipModuleProcessor;

  @MockBean PopularAccaModuleProcessor popularAccaModuleProcessor;

  @Test
  public void testConsumeInParallelsWithFanZoneQuickLink() {
    Mockito.when(storageService.getLastRunTime()).thenReturn(null);
    Mockito.when(cmsService.requestPages()).thenReturn(quickLinkPages(true));
    Mockito.when(cmsService.requestSystemConfig()).thenReturn(cmsSystemConfig());
    Mockito.when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    Mockito.doReturn(getEvents())
        .when(siteServerApi)
        .getEventForType(Mockito.eq("1808,126881"), Mockito.any(SimpleFilter.class));
    Mockito.when(
            siteServerApi.getEventToOutcomeForEvent(
                Mockito.any(List.class),
                Mockito.any(SimpleFilter.class),
                Mockito.any(),
                Mockito.any()))
        .thenReturn(getEventsToOutCome());
    featuredDataConsumer.setFanzonePageId("160");
    Mockito.when(siteServerApi.getEventForType(Mockito.eq("1811,126874"), any(SimpleFilter.class)))
        .thenReturn(getLiveAndFinshedEvents());
    Mockito.when(
            siteServerApi.getEventToOutcomeForEvent(
                Mockito.any(List.class),
                Mockito.any(SimpleFilter.class),
                Mockito.any(),
                Mockito.any()))
        .thenReturn(getEventsToOutCome(), getEventsToOutComeForStartedEvents());
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());
  }

  @Test
  public void testConsumeInParallelsWithNoFanZoneQuickLink() {
    Mockito.when(storageService.getLastRunTime()).thenReturn(null);
    Mockito.when(cmsService.requestPages()).thenReturn(quickLinkPages(false));
    Mockito.when(cmsService.requestSystemConfig()).thenReturn(cmsSystemConfig());
    Mockito.when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    Mockito.when(
            siteServerApi.getEventForType(
                Mockito.eq("1808,126881"), Mockito.any(SimpleFilter.class)))
        .thenReturn(getEvents());
    Mockito.when(
            siteServerApi.getEventToOutcomeForEvent(
                Mockito.any(List.class),
                Mockito.any(SimpleFilter.class),
                Mockito.any(),
                Mockito.any()))
        .thenReturn(getEventsToOutCome());
    featuredDataConsumer.setFanzonePageId("160");
    Mockito.when(siteServerApi.getEventForType(Mockito.eq("1811,126874"), any(SimpleFilter.class)))
        .thenReturn(getLiveAndFinshedEvents());
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());
    featuredDataConsumer.setFanzonePageId("");
    FeaturedModelsData data1 = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data1.getFeaturedModels().size());
  }

  private List<SportPage> quickLinkPages(boolean isfanZone) {
    List<SportPage> sportPages = new ArrayList<>();
    SportPage page = sportsQuickLink();
    if (isfanZone) {
      page.getSportPageModules().get(0).getSportModule().setPageId("160");
    }
    sportPages.add(page);
    return sportPages;
  }

  private CmsSystemConfig cmsSystemConfig() {
    return new CmsSystemConfig();
  }

  private SportPage sportsQuickLink() {
    List<SportPageModule> sportPageModules = new ArrayList<>();
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();
    SportsQuickLink data = new SportsQuickLink();
    data.setTitle("test");
    dataItems.add(data);
    sportPageModules.add(
        new SportPageModule(
            SportModule.builder()
                .moduleType(ModuleType.QUICK_LINK)
                .sportId(160)
                .pageType(FeaturedRawIndex.PageType.eventhub)
                .id("test")
                .brand("bma")
                .title("test")
                .build(),
            Arrays.asList(
                SportsQuickLink.builder()
                    .id("test1")
                    .sportId(160)
                    .pageType(FeaturedRawIndex.PageType.eventhub)
                    .svgId("svgId")
                    .destination("dest")
                    .build())));
    sportPageModules.get(0).getPageData().get(0).setSegments(Arrays.asList("FZ001"));
    sportPageModules.get(0).getPageData().get(0).setFanzoneSegments(Arrays.asList("FZ001"));
    sportPageModules
        .get(0)
        .getPageData()
        .get(0)
        .setSegmentReferences(Arrays.asList(new SegmentReference("FZ001", 0.0)));
    SportPage sportPage = new SportPage("h3", sportPageModules);
    sportPage.setPageId("160");
    sportPage.setPageType(FeaturedRawIndex.PageType.eventhub);
    return sportPage;
  }

  private Optional<List<Event>> getEvents() {
    return Optional.ofNullable(
        TestUtils.deserializeListWithJackson(
            "featuredSiteServerFanZoneQLTest/event_with_reference_eachway_terms.json",
            Event.class));
  }

  private Optional<List<Event>> getLiveAndFinshedEvents() {
    return Optional.ofNullable(
        TestUtils.deserializeListWithJackson(
            "featuredSiteServerFanZoneQLTest/event_live_and_finished.json", Event.class));
  }

  private Optional<List<Children>> getEventsToOutCome() {
    return Optional.ofNullable(
        TestUtils.deserializeListWithJackson(
            "featuredSiteServerFanZoneQLTest/event_to_outcome.json", Children.class));
  }

  private Optional<List<Children>> getEventsToOutComeForStartedEvents() {
    return Optional.ofNullable(
        TestUtils.deserializeListWithJackson(
            "featuredSiteServerFanZoneQLTest/event_to_outcome_started.json", Children.class));
  }
}
