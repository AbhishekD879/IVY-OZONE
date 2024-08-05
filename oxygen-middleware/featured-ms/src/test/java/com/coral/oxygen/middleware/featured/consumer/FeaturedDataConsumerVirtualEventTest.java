package com.coral.oxygen.middleware.featured.consumer;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

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
import com.coral.oxygen.middleware.featured.consumer.sportpage.*;
import com.coral.oxygen.middleware.featured.consumer.sportpage.bets.PopularBetModuleProcessor;
import com.coral.oxygen.middleware.featured.consumer.sportpage.virtual.VirtualEventsModuleProcessor;
import com.coral.oxygen.middleware.featured.service.*;
import com.coral.oxygen.middleware.featured.service.injector.DFRacingEventsModuleInjector;
import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector;
import com.coral.oxygen.middleware.featured.service.injector.FeaturedCommentaryInjector;
import com.coral.oxygen.middleware.featured.service.injector.MarketsCountInjector;
import com.coral.oxygen.middleware.featured.service.injector.RacingEventsModuleInjector;
import com.coral.oxygen.middleware.featured.service.injector.SingleOutcomeEventsModuleInjector;
import com.coral.oxygen.middleware.featured.service.injector.VirtualEventDataInjector;
import com.coral.oxygen.middleware.featured.utils.FeaturedDataUtils;
import com.coral.oxygen.middleware.featured.utils.TestUtils;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.PopularBet;
import com.coral.oxygen.middleware.pojos.model.cms.featured.PopularBetConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.RecentlyPlayedGame;
import com.coral.oxygen.middleware.pojos.model.cms.featured.RpgConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPage;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModuleDataItem;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportsQuickLink;
import com.coral.oxygen.middleware.pojos.model.cms.featured.VirtualEvent;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModelsData;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType;
import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.LimitRecordsFilter;
import com.egalacoral.spark.siteserver.api.LimitToFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
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
      QuickLinkModuleProcessor.class,
      RecentlyPlayedGameModuleProcessor.class,
      DFRacingEventsModuleInjector.class,
      AemCarouselsProcessor.class,
      RacingModuleProcessor.class,
      DateTimeHelper.class,
      QueryFilterBuilder.class,
      FeaturedModelStorageService.class,
      VirtualEventsModuleProcessor.class,
      VirtualEventDataInjector.class,
      MarketsCountInjector.class,
      FanBetsFZModuleProcessor.class,
      FanzoneQuickLinkModuleProcessor.class,
      PopularBetModuleProcessor.class,
      BybWidgetProcessor.class,
      LuckyDipModuleProcessor.class
    })
public class FeaturedDataConsumerVirtualEventTest {

  @MockBean CmsService cmsService;

  @MockBean SiteServerApi siteServerApi;

  @Autowired EventDataInjector eventDataInjector;

  @Autowired VirtualEventDataInjector virtualEventDataInjector;

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

  @MockBean TeamBetsFZModuleProcessor teamBetsFZModuleProcessor;

  @MockBean FanzoneQuickLinkModuleProcessor fanzoneQuickLinkModuleProcessor;

  @MockBean FeaturedNextRacesConfigProcessor featuredNextRacesConfigProcessor;

  @MockBean PopularBetModuleProcessor popularBetModuleProcessor;

  @MockBean BybWidgetProcessor BybWidgetProcessor;

  @MockBean LuckyDipModuleProcessor luckyDipModuleProcessor;

  @MockBean PopularAccaModuleProcessor popularAccaModuleProcessor;

  @Test
  public void testConsumeInParallels() {
    when(storageService.getLastRunTime()).thenReturn(null);
    when(cmsService.requestPages()).thenReturn(sportPages());
    when(cmsService.requestSystemConfig()).thenReturn(cmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    when(siteServerApi.getEventForType(Mockito.eq("1808,126881"), Mockito.any(SimpleFilter.class)))
        .thenReturn(getEvents());

    when(siteServerApi.getNextNEventToOutcomeForType(
            Mockito.anyInt(),
            any(List.class),
            any(SimpleFilter.class),
            any(ExistsFilter.class),
            any(LimitToFilter.class),
            any(LimitRecordsFilter.class),
            any(Boolean.class),
            any(Boolean.class)))
        .thenReturn(getEventsToOutCome(), getEventsToOutComeForStartedEvents());
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(3, data.getFeaturedModels().size());

    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(false);
    data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(0, data.getFeaturedModels().size());
  }

  @Test
  public void testConsumeInParallelsForSportPageJson() {
    when(storageService.getLastRunTime()).thenReturn(null);
    when(cmsService.requestPages()).thenReturn(getSportPages());
    when(cmsService.requestSystemConfig()).thenReturn(cmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    when(siteServerApi.getEventForType(Mockito.any(String.class), Mockito.any(SimpleFilter.class)))
        .thenReturn(getEvents());

    when(siteServerApi.getNextNEventToOutcomeForType(
            Mockito.anyInt(),
            any(List.class),
            any(SimpleFilter.class),
            any(ExistsFilter.class),
            any(LimitToFilter.class),
            any(LimitRecordsFilter.class),
            any(Boolean.class),
            any(Boolean.class)))
        .thenReturn(getEventsToOutCome());
    when(siteServerApi.getEventToOutcomeForEvent(
            Mockito.any(List.class), Mockito.any(SimpleFilter.class), Mockito.any(), Mockito.any()))
        .thenReturn(getEventsToOutComeForEvent());
    ;

    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(11, data.getFeaturedModels().size());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(false);
    data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(0, data.getFeaturedModels().size());
  }

  private List<SportPage> getSportPages() {
    return FeaturedDataUtils.getCmsSportPagesFromResource(
        "featured_consumption_cms_sportPages_output_with_virtual_next_events.json");
  }

  private List<SportPage> sportPages() {
    List<SportPage> sportPages = new ArrayList<>();

    sportPages.add(sportsQuickLink());
    sportPages.add(sportPageRPG());
    sportPages.add(virtualEventswithEventIds());
    sportPages.add(popularBets());

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
                .sportId(3)
                .pageType(PageType.eventhub)
                .id("test")
                .brand("bma")
                .title("test")
                .build(),
            Arrays.asList(
                SportsQuickLink.builder()
                    .id("test1")
                    .sportId(3)
                    .pageType(PageType.eventhub)
                    .svgId("svgId")
                    .destination("dest")
                    .build())));
    SportPage sportPage = new SportPage("h3", sportPageModules);
    sportPage.setPageId("3");
    sportPage.setPageType(PageType.eventhub);
    return sportPage;
  }

  private SportPage virtualEventswithEventIds() {
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();

    VirtualEvent virtualEvent = new VirtualEvent();
    virtualEvent.setId("65117c2dc8090c5a31a4502e");
    virtualEvent.setPageType(PageType.sport);
    virtualEvent.setType("type");
    virtualEvent.setLimit(12);
    virtualEvent.setTypeIds("1808,126881");

    VirtualEvent virtualEvent2 = new VirtualEvent();
    virtualEvent2.setId("65117c2dc8090c5a31a4502e");
    virtualEvent2.setPageType(PageType.sport);
    virtualEvent2.setType("type");
    virtualEvent2.setLimit(3);
    virtualEvent2.setTypeIds("1811,126874");

    // add
    dataItems.add(virtualEvent);
    dataItems.add(virtualEvent2);

    SportPageModule module =
        new SportPageModule(
            SportModule.builder()
                .moduleType(ModuleType.VIRTUAL_NEXT_EVENTS)
                .sportId(39)
                .pageType(PageType.sport)
                .id("virtual_next_event")
                .brand("bma")
                .title("Virtual Next Events Module")
                .build(),
            dataItems);

    return new SportPage("39", List.of(module));
  }

  private SportPage popularBets() {
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();

    PopularBet popularBet = new PopularBet();
    popularBet.setId("65117c2dc8090c5a31a4502e");
    popularBet.setPageType(PageType.sport);
    popularBet.setType("type");
    popularBet.setPopularBetConfig(createPopularBetConfig());
    // add
    dataItems.add(popularBet);

    SportPageModule module =
        new SportPageModule(
            SportModule.builder()
                .moduleType(ModuleType.POPULAR_BETS)
                .sportId(10)
                .pageType(PageType.sport)
                .id("Popular_bets")
                .brand("bma")
                .title("Popular Bets")
                .build(),
            dataItems);

    return new SportPage("39", List.of(module));
  }

  private PopularBetConfig createPopularBetConfig() {
    PopularBetConfig config = new PopularBetConfig();
    config.setEventStartsIn("24");
    config.setDisplayName("test bet");
    config.setMaxSelections(2);
    config.setMostBackedIn("24");
    config.setBackedInTimes("5 times");
    config.setMaxSelections(6);
    return config;
  }

  private SportPage sportPageRPG() {
    List<SportPageModule> sportPageModules = new ArrayList<>();
    List<SportPageModuleDataItem> dataItems = new ArrayList<>();
    RecentlyPlayedGame rpgModule = new RecentlyPlayedGame();

    RpgConfig rpgConfig = new RpgConfig();
    rpgConfig.setSeeMoreLink("link");
    rpgConfig.setGamesAmount(2);
    rpgModule.setRpgConfig(rpgConfig);
    dataItems.add(rpgModule);

    SportModule sportModule = new SportModule();
    sportModule.setModuleType(ModuleType.RECENTLY_PLAYED_GAMES);

    sportPageModules.add(new SportPageModule(sportModule, dataItems));

    SportPage sportPage = new SportPage("0", sportPageModules);
    sportPage.setPageId("0");
    sportPage.setPageType(PageType.sport);

    return sportPage;
  }

  private Optional<List<Event>> getEvents() {
    return Optional.ofNullable(
        TestUtils.deserializeListWithJackson(
            "FeaturedVirtualSiteServerServiceTest/event_with_reference_eachway_terms.json",
            Event.class));
  }

  private Optional<List<Event>> getLiveAndFinshedEvents() {
    return Optional.ofNullable(
        TestUtils.deserializeListWithJackson(
            "FeaturedVirtualSiteServerServiceTest/event_live_and_finished.json", Event.class));
  }

  private Optional<List<Event>> getEventsToOutCome() {
    return Optional.ofNullable(
        TestUtils.deserializeListWithJackson(
                "FeaturedVirtualSiteServerServiceTest/event_to_outcome_forEvent.json",
                Children.class)
            .stream()
            .map(Children::getEvent)
            .collect(Collectors.toList()));
  }

  private Optional<List<Children>> getEventsToOutComeForEvent() {
    return Optional.ofNullable(
        TestUtils.deserializeListWithJackson(
            "FeaturedVirtualSiteServerServiceTest/event_to_outcome_forEvent.json", Children.class));
  }

  private Optional<List<Event>> getEventsToOutComeForStartedEvents() {
    return Optional.ofNullable(
        TestUtils.deserializeListWithJackson(
                "FeaturedVirtualSiteServerServiceTest/event_to_outcome_forEvent_started.json",
                Children.class)
            .stream()
            .map(Children::getEvent)
            .collect(Collectors.toList()));
  }
}
