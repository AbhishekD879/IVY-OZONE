package com.coral.oxygen.middleware.featured.consumer;

import static org.assertj.core.api.Assertions.assertThat;
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
import com.coral.oxygen.middleware.featured.service.BybService;
import com.coral.oxygen.middleware.featured.service.FeaturedDataFilter;
import com.coral.oxygen.middleware.featured.service.FeaturedModelStorageService;
import com.coral.oxygen.middleware.featured.service.SportPageFilter;
import com.coral.oxygen.middleware.featured.service.injector.DFRacingEventsModuleInjector;
import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector;
import com.coral.oxygen.middleware.featured.service.injector.FeaturedCommentaryInjector;
import com.coral.oxygen.middleware.featured.service.injector.MarketsCountInjector;
import com.coral.oxygen.middleware.featured.service.injector.RacingEventsModuleInjector;
import com.coral.oxygen.middleware.featured.service.injector.SingleOutcomeEventsModuleInjector;
import com.coral.oxygen.middleware.featured.utils.TestUtils;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.Module;
import com.coral.oxygen.middleware.pojos.model.cms.ModuleDataSelection;
import com.coral.oxygen.middleware.pojos.model.cms.featured.*;
import com.coral.oxygen.middleware.pojos.model.cms.featured.RpgConfig;
import com.coral.oxygen.middleware.pojos.model.output.AssetManagement;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.*;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
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
      FanzoneQuickLinkModuleProcessor.class,
      PopularBetModuleProcessor.class,
      RecentlyPlayedGameModuleProcessor.class,
      DFRacingEventsModuleInjector.class,
      AemCarouselsProcessor.class,
      RacingModuleProcessor.class,
      DateTimeHelper.class,
      QueryFilterBuilder.class,
      FeaturedModelStorageService.class,
      FeaturedNextRacesConfigProcessor.class,
      BybWidgetProcessor.class,
      LuckyDipModuleProcessor.class
    })
public class FeaturedDataConsumerTest {

  @MockBean CmsService cmsService;

  @MockBean SiteServerApi siteServerApi;

  @Autowired EventDataInjector eventDataInjector;

  @Autowired DateTimeHelper dateTimeHelper;

  @Autowired SingleOutcomeEventsModuleInjector singleOutcomeDataInjector;

  @MockBean RacingEventsModuleInjector racingDataInjector;

  @MockBean DFRacingEventsModuleInjector dfRacingEventsModuleInjector;

  @MockBean MarketsCountInjector marketsCountInjector;

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

  @MockBean FeaturedNextRacesConfigProcessor nextRacesConfigProcessor;

  @MockBean FanBetsFZModuleProcessor fanBetsFZModuleProcessor;
  @MockBean TeamBetsFZModuleProcessor teamBetsFZModuleProcessor;

  @MockBean VirtualEventsModuleProcessor virtualEventsModuleProcessor;

  @MockBean PopularBetModuleProcessor popularBetModuleProcessor;

  @MockBean LuckyDipModuleProcessor luckyDipModuleProcessor;

  @MockBean PopularAccaModuleProcessor popularAccaModuleProcessor;

  @Test
  public void testConsumeInParallels() {
    when(storageService.getLastRunTime()).thenReturn(null);
    when(cmsService.requestPages()).thenReturn(sportPages());
    when(cmsService.requestSystemConfig()).thenReturn(cmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(3, data.getFeaturedModels().size());

    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(false);
    data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(0, data.getFeaturedModels().size());
  }

  @Test
  public void testConsumeInParallelsWithLastRunTime() {
    when(storageService.getLastRunTime()).thenReturn(Long.valueOf("1640176190014"));
    when(cmsService.requestPages(any(Long.class))).thenReturn(sportPages());
    when(cmsService.requestSystemConfig()).thenReturn(cmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(3, data.getFeaturedModels().size());

    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(false);
    data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(0, data.getFeaturedModels().size());
  }

  @Test
  public void testConsumeInParallels_whenNativeHomePageShouldNotBeSorted() {
    // given
    String[] categories =
        new String[] {
          "Football - Premier League",
          "Football - Serie A",
          "Football - Bundesliga",
          "Football - Primera Division",
          "Basketball - NBA",
          "Basketball - Euro League"
        };

    when(storageService.getLastRunTime()).thenReturn(null);
    when(systemConfigProvider.systemConfig()).thenReturn(new CmsSystemConfig());
    when(cmsService.requestPages()).thenReturn(sportPagesWithNative(categories));
    when(cmsService.requestSystemConfig()).thenReturn(cmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    List<Event> events =
        TestUtils.deserializeListWithJackson("event_from_ss_by_eventId.json", Event.class);
    Children child = new Children();
    child.setEvent(events.get(0));
    List<Children> children = new ArrayList<>();
    children.add(child);
    when(siteServerApi.getEventToOutcomeForEvent(any(), any(), any(), any()))
        .thenReturn(Optional.ofNullable(children));
    when(siteServerApi.getEventToOutcomeForEvent(any(), any(), any(), any()))
        .thenReturn(Optional.ofNullable(children));
    when(siteServerApi.getEventToOutcomeForOutcome(any(), any(), any()))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(any(String.class), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    featuredDataConsumer.setFanzonePageId("160");
    // when
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();

    // then
    assertThat(data).isNotNull();
    List<FeaturedModel> list = data.getFeaturedModels();
    Assert.assertEquals(1, list.size());
    FeaturedModel featuredModel = list.get(0);

    String[] actualCategories =
        featuredModel.getModules().stream()
            .map(module -> module.getData().get(0))
            .map(e -> ((EventsModuleData) e).getCategoryName())
            .toArray(String[]::new);

    assertThat(actualCategories).isEqualTo(categories);
  }

  @Test
  public void testConsumeInParallels_for_segmentedpage() {
    List<Event> events =
        TestUtils.deserializeListWithJackson("event_from_ss_by_eventId.json", Event.class);
    List<SportPage> sportPages = new ArrayList<>();
    sportPages.add(createSportPage());
    Children child = new Children();
    child.setEvent(events.get(0));
    List<Children> children = new ArrayList<>();
    children.add(child);
    when(siteServerApi.getEventToOutcomeForEvent(any(), any(), any(), any()))
        .thenReturn(Optional.ofNullable(children));
    when(siteServerApi.getEventToOutcomeForEvent(any(), any(), any(), any()))
        .thenReturn(Optional.ofNullable(children));
    when(storageService.getLastRunTime()).thenReturn(null);
    when(cmsService.requestPages()).thenReturn(sportPages);
    when(cmsService.requestSystemConfig()).thenReturn(cmsSystemConfig());
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig();
    when(systemConfigProvider.systemConfig()).thenReturn(new CmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    when(siteServerApi.getEventToOutcomeForOutcome(any(), any(), any()))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(any(String.class), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());
  }

  @Test
  public void testConsumeInParallels_for_segmentedpage0() {
    List<Event> events =
        TestUtils.deserializeListWithJackson("event_from_ss_by_eventId.json", Event.class);
    List<SportPage> sportPages = new ArrayList<>();
    sportPages.add(createSportPage0());
    Children child = new Children();
    child.setEvent(events.get(0));
    List<Children> children = new ArrayList<>();
    children.add(child);
    when(siteServerApi.getEventToOutcomeForEvent(any(), any(), any(), any()))
        .thenReturn(Optional.ofNullable(children));
    when(siteServerApi.getEventToOutcomeForEvent(any(), any(), any(), any()))
        .thenReturn(Optional.ofNullable(children));
    when(storageService.getLastRunTime()).thenReturn(null);
    when(cmsService.requestPages()).thenReturn(sportPages);
    when(cmsService.requestSystemConfig()).thenReturn(cmsSystemConfig());
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig();
    when(systemConfigProvider.systemConfig()).thenReturn(new CmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    when(siteServerApi.getEventToOutcomeForOutcome(any(), any(), any()))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(any(String.class), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());
  }

  @Test
  public void testConsumeInParallels_for_segmentedpage_with_moduleSegmentView() {
    List<Event> events =
        TestUtils.deserializeListWithJackson("event_from_ss_by_eventId.json", Event.class);
    List<SportPage> sportPages = new ArrayList<>();
    sportPages.add(createSportPageWithModuleSegmentView());
    Children child = new Children();
    child.setEvent(events.get(0));
    List<Children> children = new ArrayList<>();
    children.add(child);
    when(siteServerApi.getEventToOutcomeForEvent(any(), any(), any(), any()))
        .thenReturn(Optional.ofNullable(children));
    when(siteServerApi.getEventToOutcomeForEvent(any(), any(), any(), any()))
        .thenReturn(Optional.ofNullable(children));
    when(storageService.getLastRunTime()).thenReturn(null);
    when(cmsService.requestPages()).thenReturn(sportPages);
    when(cmsService.requestSystemConfig()).thenReturn(cmsSystemConfig());
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig();
    when(systemConfigProvider.systemConfig()).thenReturn(new CmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    when(siteServerApi.getEventToOutcomeForOutcome(any(), any(), any()))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(any(String.class), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    when(assetManagementService.findByTeamNameAndSportId(
            "Nathan Market".toUpperCase(Locale.ROOT), "16"))
        .thenReturn(Optional.of(getAssetManagement()));
    when(assetManagementService.findByTeamNameAndSportId(
            "NathanMeerkat".toUpperCase(Locale.ROOT), "16"))
        .thenReturn(Optional.of(getAssetManagement()));
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());
  }

  @Test
  public void testConsumeInParallels_for_segmentedpageForUSSport() {
    List<Event> events =
        TestUtils.deserializeListWithJackson("event_from_ss_by_eventId_us.json", Event.class);
    List<SportPage> sportPages = new ArrayList<>();
    sportPages.add(createSportPage());
    Children child = new Children();
    child.setEvent(events.get(0));
    List<Children> children = new ArrayList<>();
    children.add(child);
    when(siteServerApi.getEventToOutcomeForEvent(any(), any(), any(), any()))
        .thenReturn(Optional.ofNullable(children));
    when(siteServerApi.getEventToOutcomeForEvent(any(), any(), any(), any()))
        .thenReturn(Optional.ofNullable(children));
    when(storageService.getLastRunTime()).thenReturn(null);
    when(cmsService.requestPages()).thenReturn(sportPages);
    when(cmsService.requestSystemConfig()).thenReturn(cmsSystemConfig());
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig();
    when(systemConfigProvider.systemConfig()).thenReturn(new CmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    when(siteServerApi.getEventToOutcomeForOutcome(any(), any(), any()))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(any(String.class), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());
  }

  @Test
  public void testConsumeInParallels_for_segmentedpageForUSSportFot_US() {
    List<Event> events =
        TestUtils.deserializeListWithJackson("event_from_ss_by_eventId_us1.json", Event.class);
    List<SportPage> sportPages = new ArrayList<>();
    sportPages.add(createSportPage());
    Children child = new Children();
    child.setEvent(events.get(0));
    List<Children> children = new ArrayList<>();
    children.add(child);
    when(siteServerApi.getEventToOutcomeForEvent(any(), any(), any(), any()))
        .thenReturn(Optional.ofNullable(children));
    when(siteServerApi.getEventToOutcomeForEvent(any(), any(), any(), any()))
        .thenReturn(Optional.ofNullable(children));
    when(storageService.getLastRunTime()).thenReturn(null);
    when(cmsService.requestPages()).thenReturn(sportPages);
    when(cmsService.requestSystemConfig()).thenReturn(cmsSystemConfig());
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig();
    when(systemConfigProvider.systemConfig()).thenReturn(new CmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    when(siteServerApi.getEventToOutcomeForOutcome(any(), any(), any()))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(any(String.class), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    when(assetManagementService.findByTeamNameAndSportId(
            "Nathan Market".toUpperCase(Locale.ROOT), "16"))
        .thenThrow(new RuntimeException());
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());
  }

  @Test
  public void testConsumeInParallelsWithLDModule() throws Exception {
    when(storageService.getLastRunTime()).thenReturn(null);
    when(cmsService.requestPages()).thenReturn(List.of(sportsLdModule()));
    when(cmsService.requestSystemConfig()).thenReturn(cmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    featuredDataConsumer.setFanzonePageId("160");
    when(luckyDipModuleProcessor.processModule(any(), any(), any())).thenReturn(createLDModule());
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());
  }

  private List<SportPage> sportPages() {
    List<SportPage> sportPages = new ArrayList<>();

    sportPages.add(sportsQuickLink());
    sportPages.add(sportPageRPG());
    sportPages.add(getSupperButton());

    return sportPages;
  }

  private SportPage getSupperButton() {
    List<SportPageModule> sportPageModules = new ArrayList<>();
    List<SportPageModuleDataItem> dataItems = new ArrayList<>();
    SuperButton superButton = new SuperButton();
    superButton.setSportId(0);
    dataItems.add(superButton);

    SportModule sportModule = new SportModule();
    sportModule.setModuleType(ModuleType.SUPER_BUTTON);

    sportPageModules.add(new SportPageModule(sportModule, dataItems));

    SportPage sportPage = new SportPage("0", sportPageModules);
    sportPage.setPageId("0");
    sportPage.setPageType(PageType.sport);

    return sportPage;
  }

  private LuckyDipModule createLDModule() {
    LuckyDipModule luckyDipModule = new LuckyDipModule();
    luckyDipModule.setData(List.of(createluckyDipCategoryData()));
    return luckyDipModule;
  }

  private LuckyDipCategoryData createluckyDipCategoryData() {
    LuckyDipCategoryData luckyDipCategoryData = new LuckyDipCategoryData();
    luckyDipCategoryData.setSportName("|Football|");
    luckyDipCategoryData.setLuckyDipTypeData(new ArrayList<>());
    return luckyDipCategoryData;
  }

  private SportPage sportsLdModule() {
    List<SportPageModule> sportPageModules = new ArrayList<>();
    SportModule sportModule = new SportModule();
    sportModule.setModuleType(ModuleType.LUCKY_DIP);

    sportPageModules.add(new SportPageModule(sportModule, new ArrayList<>()));

    SportPage sportPage = new SportPage("0", sportPageModules);
    sportPage.setPageId("0");
    sportPage.setPageType(PageType.sport);

    return sportPage;
  }

  private CmsSystemConfig cmsSystemConfig() {
    return new CmsSystemConfig();
  }

  private List<SportPage> sportPagesWithNative(String... categories) {
    List<SportPage> sportPages = new ArrayList<>();
    sportPages.add(nativeHomePage(categories));
    return sportPages;
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

  private SportPage nativeHomePage(String... categories) {

    List<Module> modules = new LinkedList<>();
    for (String league : categories) {
      EventsModuleData eventsModuleData = new EventsModuleData();
      eventsModuleData.setCategoryName(league);
      eventsModuleData.setTypeId("1");
      eventsModuleData.setId(Long.valueOf("813059"));

      List<EventsModuleData> eventsModuleDatas = new LinkedList<>();
      eventsModuleDatas.add(eventsModuleData);

      ModuleDataSelection moduleDataSelection = new ModuleDataSelection();
      moduleDataSelection.setSelectionType("");

      Module module = new Module();
      module.setDataSelection(moduleDataSelection);
      module.setGroupedBySport(true);
      module.setData(eventsModuleDatas);

      modules.add(module);
    }

    ModularContentItem ungroupedFeaturedItem = new ModularContentItem();
    ungroupedFeaturedItem.setDirectiveName("Featured");
    ungroupedFeaturedItem.setModules(modules);

    List<SportPageModuleDataItem> ungroupedFeaturedItems = new ArrayList<>();
    ungroupedFeaturedItems.add(ungroupedFeaturedItem);

    SportModule ungroupedFeatured = new SportModule();
    ungroupedFeatured.setModuleType(ModuleType.UNGROUPED_FEATURED);
    ungroupedFeatured.setSportId(16);

    List<SportPageModule> sportPageModules = new ArrayList<>();
    sportPageModules.add(new SportPageModule(ungroupedFeatured, ungroupedFeaturedItems));

    SportPage sportPage = new SportPage("c0", sportPageModules);
    sportPage.setPageId("c0");
    sportPage.setPageType(PageType.sport);
    sportPage.setSegmented(false);

    return sportPage;
  }

  private SportPage createSportPage() {
    List<SportPageModule> sportPageModules = new ArrayList<>();
    sportPageModules.add(segmentedQuickLink(1));
    sportPageModules.add(segmentedSurfaceBet(1));
    sportPageModules.add(segmentedHighlightCarousel(1));
    sportPageModules.add(segmentedFeaturedModule(1));
    sportPageModules.add(segmentedFeaturedModule(1));
    SportPage sportPage = new SportPage("0", sportPageModules);
    sportPage.setPageId("0");
    sportPage.setPageType(PageType.sport);
    sportPage.setSegmented(true);
    return sportPage;
  }

  private SportPage createSportPage0() {
    List<SportPageModule> sportPageModules = new ArrayList<>();
    sportPageModules.add(segmentedQuickLink(1));
    sportPageModules.add(segmentedSurfaceBet(1));
    sportPageModules.add(segmentedHighlightCarousel(1));
    sportPageModules.add(segmentedFeaturedModule(1));
    sportPageModules.add(segmentedInplay(1));
    sportPageModules.add(cretaeSportModuleBybWidget(true, 1));
    sportPageModules.add(createPopularAccaModule());

    SportPage sportPage = new SportPage("0", sportPageModules);
    sportPage.setPageId("0");
    sportPage.setPageType(PageType.sport);
    sportPage.setSegmented(true);
    sportPageModules.get(1).getSportModule().setPageId("0");
    return sportPage;
  }

  private SportPage createSportPageWithModuleSegmentView() {
    List<SportPageModule> sportPageModules = new ArrayList<>();
    sportPageModules.add(segmentedQuickLink(-1));
    sportPageModules.add(segmentedSurfaceBet(-1));
    sportPageModules.add(segmentedHighlightCarousel(-1));
    sportPageModules.add(segmentedFeaturedModule(-1));
    SportPage sportPage = new SportPage("0", sportPageModules);
    sportPage.setPageId("0");
    sportPage.setPageType(PageType.sport);
    sportPage.setSegmented(true);
    return sportPage;
  }

  private SportPageModule segmentedQuickLink(double displayOrder) {
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();

    SportsQuickLink data1 =
        SportsQuickLink.builder()
            .id("test1")
            .sportId(0)
            .pageType(PageType.sport)
            .svgId("svgId")
            .destination("dest1")
            .build();

    data1.setTitle("test");
    data1.setDisplayOrder(2);
    data1.setSegments(Arrays.asList("Universal", "test"));
    SegmentReference segmentReference1 = new SegmentReference();
    segmentReference1.setDisplayOrder(displayOrder);
    segmentReference1.setSegment("Universal");
    data1.setSegmentReferences(Arrays.asList(segmentReference1));

    SportsQuickLink data2 =
        SportsQuickLink.builder()
            .id("test2")
            .sportId(0)
            .pageType(PageType.sport)
            .svgId("svgId")
            .destination("dest2")
            .build();

    data2.setTitle("test2");
    data2.setDisplayOrder(2);
    data2.setSegments(Arrays.asList("Universal", "test"));
    SegmentReference segmentReference = new SegmentReference();
    segmentReference.setDisplayOrder(Double.valueOf(2));
    segmentReference.setSegment("Universal");
    data2.setSegmentReferences(Arrays.asList(segmentReference));

    dataItems.add(data1);
    dataItems.add(data2);

    return new SportPageModule(
        SportModule.builder()
            .moduleType(ModuleType.QUICK_LINK)
            .sportId(0)
            .pageType(PageType.sport)
            .id("test")
            .brand("bma")
            .title("test")
            .build(),
        dataItems);
  }

  private SportPageModule segmentedInplay(double displayOrder) {
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();
    InplayDataSportItem inplayDataSportItem = new InplayDataSportItem();
    inplayDataSportItem.setCategoryId(16);
    inplayDataSportItem.setEventCount(2);
    inplayDataSportItem.setSportNumber(1);
    inplayDataSportItem.setSegments(Arrays.asList("Universal", "test"));
    SegmentReference segReference = new SegmentReference();
    segReference.setDisplayOrder(displayOrder);
    segReference.setSegment("Universal");
    inplayDataSportItem.setSegmentReferences(Arrays.asList(segReference));
    List<InplayDataSportItem> homeInplaySports = new ArrayList<>();
    homeInplaySports.add(inplayDataSportItem);

    InPlayConfig data1 = new InPlayConfig();
    data1.setSportId(0);
    data1.setPageType(PageType.sport);
    data1.setMaxEventCount(10);

    data1.setSegments(Arrays.asList("Universal", "test"));
    SegmentReference segmentReference1 = new SegmentReference();
    segmentReference1.setDisplayOrder(displayOrder);
    segmentReference1.setSegment("Universal");
    data1.setSegmentReferences(Arrays.asList(segmentReference1));
    data1.setHomeInplaySports(homeInplaySports);

    InPlayConfig data2 = new InPlayConfig();
    data2.setSportId(0);
    data2.setPageType(PageType.sport);
    data2.setMaxEventCount(10);

    data2.setSegments(Arrays.asList("Universal", "test"));
    SegmentReference segmentReference = new SegmentReference();
    segmentReference.setDisplayOrder(Double.valueOf(2));
    segmentReference.setSegment("Universal");
    data2.setSegmentReferences(Arrays.asList(segmentReference));
    data2.setHomeInplaySports(homeInplaySports);

    dataItems.add(data1);
    dataItems.add(data2);

    return new SportPageModule(
        SportModule.builder()
            .moduleType(ModuleType.INPLAY)
            .sportId(0)
            .pageType(PageType.sport)
            .id("test")
            .brand("bma")
            .title("test")
            .build(),
        dataItems);
  }

  private SportPageModule segmentedSurfaceBet(double displayOrder) {
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();

    SurfaceBet sb = new SurfaceBet();
    sb.setId("sb");
    sb.setPageType(PageType.sport);
    sb.setSvgId("svgId");

    sb.setTitle("sb");
    sb.setDisplayOrder(2);
    sb.setSelectionId(BigInteger.valueOf(483998812));
    sb.setSegments(Arrays.asList("Universal", "test-one"));
    SegmentReference segmentReference = new SegmentReference();
    segmentReference.setDisplayOrder(displayOrder);
    segmentReference.setSegment("Universal");
    sb.setSegmentReferences(Arrays.asList(segmentReference));

    SurfaceBet sb2 = new SurfaceBet();
    sb2.setId("sb2");
    sb2.setPageType(PageType.sport);
    sb2.setSvgId("svgId");

    sb2.setTitle("sb2");
    sb2.setDisplayOrder(1);
    sb2.setSelectionId(BigInteger.valueOf(483998812));
    sb2.setSegments(Arrays.asList("Universal", "test-one"));
    SegmentReference segmentReference2 = new SegmentReference();
    segmentReference2.setDisplayOrder(displayOrder);
    segmentReference2.setSegment("Universal");
    sb2.setSegmentReferences(Arrays.asList(segmentReference2));

    dataItems.add(sb);
    dataItems.add(sb2);
    return new SportPageModule(
        SportModule.builder()
            .moduleType(ModuleType.SURFACE_BET)
            .sportId(0)
            .pageType(PageType.sport)
            .id("sb")
            .brand("bma")
            .title("sb")
            .build(),
        dataItems);
  }

  private SportPageModule segmentedHighlightCarousel(double displayOrder) {
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();

    HighlightCarousel hc = new HighlightCarousel();
    hc.setId("hc");
    hc.setPageType(PageType.sport);
    hc.setSvgId("svgId");

    hc.setTitle("hc");
    hc.setDisplayOrder(3);
    // hc.setEvents(Arrays.asList("8130591"));
    hc.setType("type");
    hc.setTypeId(12);
    hc.setSegments(Arrays.asList("Universal", "Universal", "test-two"));
    SegmentReference segmentReference = new SegmentReference();
    segmentReference.setDisplayOrder(displayOrder);
    segmentReference.setSegment("Universal");
    hc.setSegmentReferences(Arrays.asList(segmentReference));

    HighlightCarousel hc2 = new HighlightCarousel();
    hc2.setId("hc2");
    hc2.setPageType(PageType.sport);
    hc2.setSvgId("svgId");

    hc2.setTitle("hc2");
    hc2.setDisplayOrder(3);
    // hc.setEvents(Arrays.asList("8130591"));
    hc2.setType("type");
    hc2.setTypeId(12);
    hc2.setSegments(Arrays.asList("Universal", "Universal", "test-two"));
    SegmentReference segmentReference2 = new SegmentReference();
    segmentReference2.setDisplayOrder(displayOrder);
    segmentReference2.setSegment("Universal");
    hc2.setSegmentReferences(Arrays.asList(segmentReference2));

    HighlightCarousel hc3 = new HighlightCarousel();
    hc3.setId("hc3");
    hc3.setPageType(PageType.sport);
    hc3.setSvgId("svgId");
    hc3.setDisplayMarketType("2UpMarket");
    hc3.setTitle("hc3");
    hc3.setDisplayOrder(3);
    // hc.setEvents(Arrays.asList("8130591"));
    hc3.setType("type");
    hc3.setTypeId(12);
    hc3.setSegments(Arrays.asList("Universal", "Universal", "test-two"));
    SegmentReference segmentReference3 = new SegmentReference();
    segmentReference3.setDisplayOrder(displayOrder);
    segmentReference3.setSegment("Universal");
    hc3.setSegmentReferences(Arrays.asList(segmentReference3));

    dataItems.add(hc);
    dataItems.add(hc2);
    dataItems.add(hc3);

    return new SportPageModule(
        SportModule.builder()
            .moduleType(ModuleType.HIGHLIGHTS_CAROUSEL)
            .sportId(0)
            .pageType(PageType.sport)
            .id("hc")
            .brand("bma")
            .title("hc")
            .build(),
        dataItems);
  }

  private SportPageModule segmentedFeaturedModule(double displayOrder) {

    List<Module> modules = new LinkedList<>();
    EventsModuleData eventsModuleData = new EventsModuleData();
    eventsModuleData.setCategoryName("Football - Premier League");
    eventsModuleData.setTypeId("1");
    eventsModuleData.setId(Long.valueOf("813059"));
    eventsModuleData.setName("Arsinel vs Liverpool");
    eventsModuleData.setCategoryId("16");
    eventsModuleData.setCategoryCode("16");
    List<EventsModuleData> eventsModuleDatas = new LinkedList<>();
    eventsModuleDatas.add(eventsModuleData);

    ModuleDataSelection moduleDataSelection = new ModuleDataSelection();
    moduleDataSelection.setSelectionType("");

    Module module = new Module();
    module.setDataSelection(moduleDataSelection);
    module.setGroupedBySport(true);
    module.setData(eventsModuleDatas);
    module.set_id("1234");
    module.setDisplayOrder(new BigDecimal(4));
    module.setSegments(Arrays.asList("Universal", "test-three"));
    SegmentReference segmentReference = new SegmentReference();
    segmentReference.setDisplayOrder(displayOrder);
    segmentReference.setSegment("Universal");
    module.setSegmentReferences(Arrays.asList(segmentReference));
    module.setMaxRows(0);

    Module module2 = new Module();
    module2.setDataSelection(moduleDataSelection);
    module2.setGroupedBySport(true);
    module2.setData(eventsModuleDatas);
    module2.set_id("1234");
    module2.setDisplayOrder(new BigDecimal(4));
    module2.setSegments(Arrays.asList("Universal", "Universal", "test-four"));
    SegmentReference segmentReference2 = new SegmentReference();
    segmentReference2.setDisplayOrder(displayOrder);
    segmentReference2.setSegment("Universal");
    module2.setSegmentReferences(Arrays.asList(segmentReference2));
    module2.setMaxRows(3);

    Module module3 = new Module();
    module3.setDataSelection(moduleDataSelection);
    module3.setGroupedBySport(true);
    module3.setData(eventsModuleDatas);
    module3.set_id("1234");
    module3.setDisplayOrder(new BigDecimal(4));
    module3.setSegments(Arrays.asList("Universal", "Universal", "test-four"));
    SegmentReference segmentReference3 = new SegmentReference();
    segmentReference3.setDisplayOrder(displayOrder);
    segmentReference3.setSegment("Universal");
    module3.setSegmentReferences(Arrays.asList(segmentReference3));
    module3.setMaxRows(null);

    modules.add(module);
    modules.add(module2);
    modules.add(module3);

    ModularContentItem ungroupedFeaturedItem = new ModularContentItem();
    ungroupedFeaturedItem.setDirectiveName("Featured");
    ungroupedFeaturedItem.setTitle("featured");
    ungroupedFeaturedItem.setModules(modules);

    List<SportPageModuleDataItem> ungroupedFeaturedItems = new ArrayList<>();
    ungroupedFeaturedItems.add(ungroupedFeaturedItem);

    return new SportPageModule(
        SportModule.builder()
            .moduleType(ModuleType.UNGROUPED_FEATURED)
            .sportId(0)
            .pageType(PageType.sport)
            .id("featured")
            .brand("bma")
            .title("featured")
            .build(),
        ungroupedFeaturedItems);
  }

  private AssetManagement getAssetManagement() {
    AssetManagement assetManagement = new AssetManagement();
    assetManagement.setTeamName("Arsinel");
    return assetManagement;
  }

  private SportPageModule cretaeSportModuleBybWidget(boolean showAll, int visible) {
    SportModule module =
        new SportModule(
            FeaturedRawIndex.PageType.sport,
            "123",
            0,
            0.0,
            true,
            "0",
            "title",
            "ladbrokes",
            ModuleType.BYB_WIDGET,
            new ArrayList<>());
    List<SportPageModuleDataItem> widgetModule = createBYbWwidget(showAll, visible);
    SportPageModule sportPageModule = new SportPageModule(module, widgetModule);
    return sportPageModule;
  }

  private SportPageModule createPopularAccaModule() {
    SportModule module =
        new SportModule(
            FeaturedRawIndex.PageType.sport,
            "123",
            0,
            0.0,
            true,
            "0",
            "title",
            "ladbrokes",
            ModuleType.POPULAR_ACCA,
            new ArrayList<>());
    List<SportPageModuleDataItem> widgetModule = createPopularAccaWwidget();
    return new SportPageModule(module, widgetModule);
  }

  private List<SportPageModuleDataItem> createPopularAccaWwidget() {
    PopularAccaWidget widget = new PopularAccaWidget();

    widget.setTitle("title");
    widget.setPageType(FeaturedRawIndex.PageType.sport);
    widget.setData(preparePopularAccaWidgetData());
    List<SportPageModuleDataItem> list = new ArrayList<>();
    list.add(widget);
    return list;
  }

  private List<PopularAccaWidgetData> preparePopularAccaWidgetData() {
    List<PopularAccaWidgetData> widgets = new ArrayList<>();
    widgets.add(createAccaWidgetData("title-1", 1));
    return widgets;
  }

  private PopularAccaWidgetData createAccaWidgetData(String title, int sortOrder) {
    PopularAccaWidgetData data = new PopularAccaWidgetData();
    data.setTitle(title);
    data.setSortOrder(sortOrder);
    return data;
  }

  private List<SportPageModuleDataItem> createBYbWwidget(boolean showAll, int visible) {
    BybWidget widget = new BybWidget();

    widget.setId("12313131");
    widget.setTitle("title");
    widget.setShowAll(showAll);
    widget.setMarketCardVisibleSelections(visible);
    widget.setPageType(FeaturedRawIndex.PageType.sport);
    widget.setData(prepareWidgetData());
    List<SportPageModuleDataItem> list = new ArrayList<>();
    list.add(widget);
    return list;
  }

  private List<BybWidgetData> prepareWidgetData() {
    List<BybWidgetData> widgets = new ArrayList<>();
    widgets.add(createWidgetData("title-1", "125554280", "8130591", 1));
    return widgets;
  }

  private BybWidgetData createWidgetData(
      String title, String marketId, String eventId, int sortOrder) {
    BybWidgetData data = new BybWidgetData();
    data.setTitle(title);
    data.setMarketId(marketId);
    data.setEventId(eventId);
    data.setSortOrder(sortOrder);
    return data;
  }
}
