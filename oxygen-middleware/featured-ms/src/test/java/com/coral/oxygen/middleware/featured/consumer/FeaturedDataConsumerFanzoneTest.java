package com.coral.oxygen.middleware.featured.consumer;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.Mockito.when;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.cms.api.SystemConfigProvider;
import com.coral.oxygen.middleware.common.configuration.*;
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
import com.coral.oxygen.middleware.featured.service.injector.*;
import com.coral.oxygen.middleware.featured.utils.TestUtils;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.Fanzone;
import com.coral.oxygen.middleware.pojos.model.cms.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModelsData;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import java.math.BigInteger;
import java.util.*;
import org.apache.commons.lang3.text.WordUtils;
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
      RecentlyPlayedGameModuleProcessor.class,
      DFRacingEventsModuleInjector.class,
      AemCarouselsProcessor.class,
      RacingModuleProcessor.class,
      TeamBetsFZModuleProcessor.class,
      FanBetsFZModuleProcessor.class,
      DateTimeHelper.class,
      QueryFilterBuilder.class,
      FeaturedModelStorageService.class,
      FeaturedNextRacesConfigProcessor.class,
      PopularBetModuleProcessor.class,
      BybWidgetProcessor.class,
      LuckyDipModuleProcessor.class
    })
public class FeaturedDataConsumerFanzoneTest {

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

  @MockBean VirtualEventsModuleProcessor virtualEventsModuleProcessor;

  @MockBean PopularBetModuleProcessor popularBetModuleProcessor;

  @MockBean LuckyDipModuleProcessor luckyDipModuleProcessor;

  @MockBean PopularAccaModuleProcessor popularAccaModuleProcessor;

  @Test
  public void testConsumeInParallels_for_NoFanzoneValidation() {
    List<Event> events =
        TestUtils.deserializeListWithJackson("event_from_ss_by_eventId.json", Event.class);
    List<SportPage> sportPages = new ArrayList<>();
    sportPages.add(createSportPage160WithTypeIds());
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
    when(cmsService.getFanzones()).thenReturn(fanzonesListForNoValidation());
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig();
    when(systemConfigProvider.systemConfig()).thenReturn(new CmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    when(siteServerApi.getEventToOutcomeForOutcome(any(), any(), any()))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(any(String.class), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(anyList(), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());
  }

  @Test
  public void testConsumeInParallelsForUnsegmentedModules() {
    when(storageService.getLastRunTime()).thenReturn(null);
    when(cmsService.requestPages()).thenReturn(sportPages());
    when(cmsService.requestSystemConfig()).thenReturn(cmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());

    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(false);
    data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(0, data.getFeaturedModels().size());
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
    when(cmsService.getFanzones()).thenReturn(fanzonesList());
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig();
    when(systemConfigProvider.systemConfig()).thenReturn(new CmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    when(siteServerApi.getEventToOutcomeForOutcome(any(), any(), any()))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(any(String.class), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(anyList(), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());
  }

  @Test
  public void testConsumeInParallels_for_segmentedpage160withTypeIds() {
    List<Event> events =
        TestUtils.deserializeListWithJackson("event_from_ss_by_eventId.json", Event.class);
    List<SportPage> sportPages = new ArrayList<>();
    sportPages.add(createSportPage160WithTypeIds());
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
    when(cmsService.getFanzones()).thenReturn(fanzonesList());
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig();
    when(systemConfigProvider.systemConfig()).thenReturn(new CmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    when(siteServerApi.getEventToOutcomeForOutcome(any(), any(), any()))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(any(String.class), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(anyList(), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());
  }

  @Test
  public void testConsumeInParallels_for_segmentedpage160withmodulepageidnot160() {
    List<Event> events =
        TestUtils.deserializeListWithJackson("event_from_ss_by_eventId.json", Event.class);
    List<SportPage> sportPages = new ArrayList<>();
    sportPages.add(createSportPage160WithModulepageIdnot160());
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
    when(cmsService.getFanzones()).thenReturn(fanzonesList());
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig();
    when(systemConfigProvider.systemConfig()).thenReturn(new CmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    when(siteServerApi.getEventToOutcomeForOutcome(any(), any(), any()))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(any(String.class), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(anyList(), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    featuredDataConsumer.setFanzonePageId("");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());
  }

  @Test
  public void testConsumeInParallels_for_segmentedpage160_notypeids_noeventids() {
    List<Event> events =
        TestUtils.deserializeListWithJackson("event_from_ss_by_eventId.json", Event.class);
    List<SportPage> sportPages = new ArrayList<>();
    sportPages.add(createSportPage160NoTypeIdsNoEventIds());
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
    when(cmsService.getFanzones()).thenReturn(fanzonesList());
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig();
    when(systemConfigProvider.systemConfig()).thenReturn(new CmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    when(siteServerApi.getEventToOutcomeForOutcome(any(), any(), any()))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(any(String.class), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(anyList(), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());
  }

  @Test
  public void testConsumeInParallels_for_segmentedpage160_withEventIds() {
    List<Event> events =
        TestUtils.deserializeListWithJackson("event_from_ss_by_eventId.json", Event.class);
    List<SportPage> sportPages = new ArrayList<>();
    sportPages.add(createSportPage160WithEventIds());
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
    when(cmsService.getFanzones()).thenReturn(fanzonesList());
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig();
    when(systemConfigProvider.systemConfig()).thenReturn(new CmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    when(siteServerApi.getEventToOutcomeForOutcome(any(), any(), any()))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(any(String.class), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(anyList(), any(SimpleFilter.class)))
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
    SportPage sportPage = createSportPageWithModuleFanzoneSegmentView();
    sportPage.setSegmented(false);
    sportPages.add(sportPage);
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
    when(cmsService.getFanzones()).thenReturn(fanzonesList());
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig();
    when(systemConfigProvider.systemConfig()).thenReturn(new CmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    when(siteServerApi.getEventToOutcomeForOutcome(any(), any(), any()))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(any(String.class), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    when(siteServerApi.getEventForType(anyList(), any(SimpleFilter.class)))
        .thenReturn(Optional.ofNullable(events));
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());
  }

  @Test
  public void testConsumeInParallels_TeamandFanBetsModule() {

    List<SportPageModule> sportPageModules = new ArrayList<>();

    sportPageModules.add(getTeamBetsFZModules(1, ModuleType.BETS_BASED_ON_YOUR_TEAM)); // 0
    sportPageModules.add(getFanBetsFZModules(1, ModuleType.BETS_BASED_ON_OTHER_FANS)); // 1
    sportPageModules.add(getTeamBetsFZModules(1, ModuleType.BETS_BASED_ON_YOUR_TEAM)); // 2
    sportPageModules.get(2).getSportModule().setPageId("60");
    sportPageModules.add(getFanBetsFZModules(1, ModuleType.BETS_BASED_ON_OTHER_FANS)); // 3
    sportPageModules.get(3).getSportModule().setPageId("60");

    SportPage sportPage = new SportPage("160", sportPageModules);
    sportPage.setPageId("160");
    sportPage.setPageType(PageType.sport);
    sportPage.setSegmented(true);
    List<SportPage> sportPages = new ArrayList<>();
    sportPages.add(sportPage);

    when(storageService.getLastRunTime()).thenReturn(null);
    when(cmsService.requestPages()).thenReturn(sportPages);
    when(cmsService.requestSystemConfig()).thenReturn(cmsSystemConfig());
    when(cmsService.getFanzones()).thenReturn(fanzonesListForNoValidation());
    when(systemConfigProvider.systemConfig()).thenReturn(new CmsSystemConfig());
    when(sportPageFilter.isSupportedPage(any(SportPage.class))).thenReturn(true);
    featuredDataConsumer.setFanzonePageId("160");
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels();
    Assert.assertEquals(1, data.getFeaturedModels().size());
  }

  private SportPage createSportPage() {
    List<SportPageModule> sportPageModules = new ArrayList<>();
    sportPageModules.add(segmentedHighlightCarouselwithTypeIds(1));
    sportPageModules.add(segmentedSurfaceBet(1));
    SportPage sportPage = new SportPage("160", sportPageModules);
    sportPage.setPageId("160");
    sportPage.setPageType(PageType.sport);
    sportPage.setSegmented(true);
    sportPageModules.get(0).getSportModule().setPageId("160");
    return sportPage;
  }

  private SportPage createSportPage160WithTypeIds() {
    List<SportPageModule> sportPageModules = new ArrayList<>();
    sportPageModules.add(segmentedHighlightCarouselwithTypeIds(1));
    sportPageModules.add(segmentedSurfaceBet(1));
    SportPage sportPage = new SportPage("160", sportPageModules);
    sportPage.setPageId("160");
    sportPage.setPageType(PageType.sport);
    sportPage.setSegmented(true);
    sportPageModules.get(1).getSportModule().setPageId("160");
    sportPageModules.get(0).getSportModule().setPageId("160");
    return sportPage;
  }

  private SportPage createSportPage160WithModulepageIdnot160() {
    List<SportPageModule> sportPageModules = new ArrayList<>();
    sportPageModules.add(segmentedHighlightCarouselwithmodulepageidnot160(1));
    sportPageModules.add(segmentedSurfaceBet(1));
    SportPage sportPage = new SportPage("160", sportPageModules);
    sportPage.setPageId("160");
    sportPage.setPageType(PageType.sport);
    sportPage.setSegmented(true);
    sportPageModules.get(1).getSportModule().setPageId("160");
    sportPageModules.get(0).getSportModule().setPageId("160");
    return sportPage;
  }

  private SportPage createSportPage160WithEventIds() {
    List<SportPageModule> sportPageModules = new ArrayList<>();
    sportPageModules.add(segmentedHighlightCarouselwithEventIds(1));
    sportPageModules.add(segmentedSurfaceBet(1));
    SportPage sportPage = new SportPage("160", sportPageModules);
    sportPage.setPageId("160");
    sportPage.setPageType(PageType.sport);
    sportPage.setSegmented(true);
    sportPageModules.get(1).getSportModule().setPageId("160");
    sportPageModules.get(0).getSportModule().setPageId("160");
    return sportPage;
  }

  private SportPage createSportPage160NoTypeIdsNoEventIds() {
    List<SportPageModule> sportPageModules = new ArrayList<>();
    sportPageModules.add(segmentedHighlightCarouselNoTypeIDsNoEventIds(1));
    sportPageModules.add(segmentedSurfaceBet(1));
    SportPage sportPage = new SportPage("160", sportPageModules);
    sportPage.setPageId("160");
    sportPage.setPageType(PageType.sport);
    sportPage.setSegmented(true);
    sportPageModules.get(1).getSportModule().setPageId("160");
    sportPageModules.get(0).getSportModule().setPageId("160");
    return sportPage;
  }

  private Fanzone createFanzone() {
    Fanzone fanzone = new Fanzone();
    fanzone.setName("Arsenal");
    fanzone.setTeamId("1001");
    fanzone.setPrimaryCompetitionId("442");
    fanzone.setSecondaryCompetitionId("443,444");
    return fanzone;
  }

  private List<Fanzone> fanzonesList() {
    List<Fanzone> fanzoneList = new ArrayList<Fanzone>();
    Fanzone f1 = createFanzone();
    Fanzone f2 = createFanzone();
    f2.setTeamId("1004");
    f2.setName("Burnley");
    Fanzone f3 = createFanzone();
    f3.setName("Chelsea");
    f3.setTeamId("1003");
    fanzoneList.add(f1);
    fanzoneList.add(f2);
    fanzoneList.add(f3);
    return fanzoneList;
  }

  private SportPage createSportPageWithModuleFanzoneSegmentView() {
    List<SportPageModule> sportPageModules = new ArrayList<>();
    sportPageModules.add(segmentedSurfaceBet(-1));
    sportPageModules.add(segmentedHighlightCarouselwithTypeIds(-1));
    SportPage sportPage = new SportPage("160", sportPageModules);
    sportPage.setPageId("160");
    sportPage.setPageType(PageType.sport);
    sportPage.setSegmented(true);
    return sportPage;
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
    List<String> fzsegments = new ArrayList<String>();
    fzsegments.add("1001");
    fzsegments.add("1002");
    fzsegments.add("1005");
    fzsegments.add("1006");
    fzsegments.add("Chennai");
    sb.setFanzoneSegments(fzsegments);
    SurfaceBet sb2 = new SurfaceBet();
    sb2.setId("sb2");
    sb2.setPageType(PageType.sport);
    sb2.setSvgId("svgId");

    sb2.setTitle("sb2");
    sb2.setDisplayOrder(1);
    sb2.setSelectionId(BigInteger.valueOf(483998812));
    List<String> fzsegments1 = new ArrayList<String>();
    fzsegments1.add("1001");
    fzsegments1.add("1002");
    fzsegments1.add("1005");
    fzsegments1.add("1006");
    sb2.setFanzoneSegments(fzsegments1);
    dataItems.add(sb);
    dataItems.add(sb2);
    return new SportPageModule(
        SportModule.builder()
            .moduleType(ModuleType.SURFACE_BET)
            .sportId(160)
            .pageType(PageType.sport)
            .id("sb")
            .brand("bma")
            .title("sb")
            .build(),
        dataItems);
  }

  private SportPageModule segmentedHighlightCarouselwithTypeIds(double displayOrder) {
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();

    HighlightCarousel hc = new HighlightCarousel();
    hc.setId("hc");
    hc.setPageType(PageType.sport);
    hc.setSvgId("svgId");
    hc.setInPlay(true);
    hc.setTitle("hc");
    hc.setType("type");
    List<String> typeIds1 = new ArrayList<String>();
    typeIds1.add("442");
    typeIds1.add("777");
    typeIds1.add("666");
    hc.setTypeIds(typeIds1);
    List<String> fzsegments1 = new ArrayList<String>();
    fzsegments1.add("1001");
    fzsegments1.add("1002");
    fzsegments1.add("1005");
    fzsegments1.add("1006");
    hc.setFanzoneSegments(fzsegments1);

    HighlightCarousel hc2 = new HighlightCarousel();
    hc2.setId("hc2");
    hc2.setPageType(PageType.sport);
    hc2.setInPlay(null);
    hc2.setSvgId("svgId");
    hc2.setTitle("hc2");
    hc2.setType("type");
    List<String> typeIds = new ArrayList<String>();
    typeIds.add("442");
    typeIds.add("8888");
    hc2.setTypeIds(typeIds);
    List<String> fzsegments = new ArrayList<String>();
    fzsegments.add("1001");
    fzsegments.add("1002");
    fzsegments.add("1003");
    fzsegments.add("1004");
    fzsegments.add("1004");
    hc2.setFanzoneSegments(fzsegments);
    dataItems.add(hc);
    dataItems.add(hc2);
    return new SportPageModule(
        SportModule.builder()
            .moduleType(ModuleType.HIGHLIGHTS_CAROUSEL)
            .sportId(160)
            .pageType(PageType.sport)
            .id("hc")
            .brand("bma")
            .title("hc")
            .build(),
        dataItems);
  }

  private SportPageModule getTeamBetsFZModules(double displayOrder, ModuleType moduleType) {
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();

    TeamBets teamBetsData = new TeamBets();
    teamBetsData.setId("TeamBetID");
    teamBetsData.setNoOfMaxSelections(4);
    teamBetsData.setSportId(160);
    teamBetsData.setTitle(
        WordUtils.capitalizeFully(moduleType.name().replace("_", " ")) + " Module");
    teamBetsData.setPageType(PageType.sport);
    teamBetsData.setFanzoneSegments(Arrays.asList("334d", "5865hf", "ufjg", "ufjg"));
    dataItems.add(teamBetsData);

    return new SportPageModule(
        SportModule.builder()
            .moduleType(moduleType)
            .sportId(160)
            .pageId("160")
            .pageType(PageType.sport)
            .id("TeamBetID")
            .brand("ladbrokes")
            .title(WordUtils.capitalizeFully(moduleType.name().replace("_", " ")) + " Module")
            .build(),
        dataItems);
  }

  private SportPageModule getFanBetsFZModules(double displayOrder, ModuleType moduleType) {
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();

    FanBets fanBetsData = new FanBets();
    fanBetsData.setId("fanBetID");
    fanBetsData.setNoOfMaxSelections(4);
    fanBetsData.setSportId(160);
    fanBetsData.setTitle(
        WordUtils.capitalizeFully(moduleType.name().replace("_", " ")) + " Module");
    fanBetsData.setPageType(PageType.sport);
    fanBetsData.setFanzoneSegments(Arrays.asList("334d", "5865hf", "ufjg", "ufjg", "8475"));
    dataItems.add(fanBetsData);

    return new SportPageModule(
        SportModule.builder()
            .moduleType(moduleType)
            .sportId(160)
            .pageId("160")
            .pageType(PageType.sport)
            .id("fanBetID")
            .brand("ladbrokes")
            .title(WordUtils.capitalizeFully(moduleType.name().replace("_", " ")) + " Module")
            .build(),
        dataItems);
  }

  private SportPageModule segmentedHighlightCarouselwithmodulepageidnot160(double displayOrder) {
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();

    HighlightCarousel hc = new HighlightCarousel();
    hc.setId("hc");
    hc.setPageType(PageType.sport);
    hc.setSvgId("svgId");
    hc.setInPlay(true);
    hc.setTitle("hc");
    hc.setType("type");
    List<String> typeIds1 = new ArrayList<String>();
    typeIds1.add("442");
    typeIds1.add("777");
    typeIds1.add("666");
    hc.setTypeIds(typeIds1);
    List<String> fzsegments1 = new ArrayList<String>();
    fzsegments1.add("1001");
    fzsegments1.add("1002");
    fzsegments1.add("1005");
    fzsegments1.add("1006");
    hc.setFanzoneSegments(fzsegments1);

    HighlightCarousel hc2 = new HighlightCarousel();
    hc2.setId("hc2");
    hc2.setPageType(PageType.sport);
    hc2.setInPlay(null);
    hc2.setSvgId("svgId");
    hc2.setTitle("hc2");
    hc2.setType("type");
    List<String> typeIds = new ArrayList<String>();
    typeIds.add("442");
    typeIds.add("8888");
    hc2.setTypeIds(typeIds);
    List<String> fzsegments = new ArrayList<String>();
    fzsegments.add("1001");
    fzsegments.add("1002");
    fzsegments.add("1003");
    fzsegments.add("1004");
    hc2.setFanzoneSegments(fzsegments);
    dataItems.add(hc);
    dataItems.add(hc2);
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

  private SportPageModule segmentedHighlightCarouselwithEventIds(double displayOrder) {
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();

    HighlightCarousel hc = new HighlightCarousel();
    hc.setId("hc");
    hc.setPageType(PageType.sport);
    hc.setSvgId("svgId");
    hc.setInPlay(true);
    hc.setTitle("hc");
    hc.setType("type");
    List<String> events = new ArrayList<String>();
    events.add("8130591");
    events.add("8130592");
    events.add("8130593");
    hc.setEvents(events);
    List<String> fzsegments1 = new ArrayList<String>();
    fzsegments1.add("1001");
    fzsegments1.add("1002");
    fzsegments1.add("1005");
    fzsegments1.add("1006");
    hc.setFanzoneSegments(fzsegments1);

    HighlightCarousel hc2 = new HighlightCarousel();
    hc2.setId("hc2");
    hc2.setPageType(PageType.sport);
    hc2.setInPlay(null);
    hc2.setSvgId("svgId");
    hc2.setTitle("hc2");
    hc2.setType("type");
    List<String> events2 = new ArrayList<String>();
    events2.add("8130591");
    events2.add("8130592");
    events2.add("8130593");
    hc2.setEvents(events2);
    List<String> fzsegments = new ArrayList<String>();
    fzsegments.add("1001");
    fzsegments.add("1002");
    fzsegments.add("1003");
    fzsegments.add("1004");
    hc2.setFanzoneSegments(fzsegments);
    dataItems.add(hc);
    dataItems.add(hc2);
    return new SportPageModule(
        SportModule.builder()
            .moduleType(ModuleType.HIGHLIGHTS_CAROUSEL)
            .sportId(160)
            .pageType(PageType.sport)
            .id("hc")
            .brand("bma")
            .title("hc")
            .build(),
        dataItems);
  }

  private SportPageModule segmentedHighlightCarouselNoTypeIDsNoEventIds(double displayOrder) {
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();

    HighlightCarousel hc = new HighlightCarousel();
    hc.setId("hc");
    hc.setPageType(PageType.sport);
    hc.setSvgId("svgId");
    hc.setInPlay(true);
    hc.setTitle("hc");
    hc.setType("type");
    List<String> emptylist = new ArrayList<String>();
    hc.setTypeIds(emptylist);
    hc.setEvents(emptylist);
    List<String> fzsegments1 = new ArrayList<String>();
    fzsegments1.add("1001");
    fzsegments1.add("1002");
    fzsegments1.add("1005");
    fzsegments1.add("1006");
    hc.setFanzoneSegments(fzsegments1);

    HighlightCarousel hc2 = new HighlightCarousel();
    hc2.setId("hc2");
    hc2.setPageType(PageType.sport);
    hc2.setInPlay(null);
    hc2.setSvgId("svgId");
    hc2.setTitle("hc2");
    hc2.setType("type");
    List<String> emptylist1 = new ArrayList<String>();
    hc2.setTypeIds(emptylist1);
    hc2.setEvents(emptylist1);
    List<String> fzsegments = new ArrayList<String>();
    fzsegments.add("1001");
    fzsegments.add("1002");
    fzsegments.add("1003");
    fzsegments.add("1004");
    hc2.setFanzoneSegments(fzsegments);
    dataItems.add(hc);
    dataItems.add(hc2);
    return new SportPageModule(
        SportModule.builder()
            .moduleType(ModuleType.HIGHLIGHTS_CAROUSEL)
            .sportId(160)
            .pageType(PageType.sport)
            .id("hc")
            .brand("bma")
            .title("hc")
            .build(),
        dataItems);
  }

  private List<SportPage> sportPages() {
    List<SportPage> sportPages = new ArrayList<>();
    sportPages.add(sportPageRPG());
    return sportPages;
  }

  private CmsSystemConfig cmsSystemConfig() {
    return new CmsSystemConfig();
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

    SportPage sportPage = new SportPage("160", sportPageModules);
    sportPage.setPageId("160");
    sportPage.setPageType(PageType.sport);

    return sportPage;
  }

  private Fanzone createFanzoneForNoValidation() {
    Fanzone fanzone = new Fanzone();
    fanzone.setName("Arsenal");
    fanzone.setPrimaryCompetitionId("442");
    fanzone.setSecondaryCompetitionId("443,444,666,777,888");
    fanzone.setTeamId("1001");
    return fanzone;
  }

  private List<Fanzone> fanzonesListForNoValidation() {
    List<Fanzone> fanzoneList = new ArrayList<Fanzone>();
    Fanzone f1 = createFanzoneForNoValidation();
    Fanzone f2 = createFanzoneForNoValidation();
    f2.setName("Everton");
    f2.setTeamId("1002");
    Fanzone f3 = createFanzoneForNoValidation();
    f3.setName("Chelsea");
    f3.setTeamId("1003");
    Fanzone f4 = createFanzoneForNoValidation();
    f4.setName("Barcelona");
    f4.setTeamId("1004");
    Fanzone f5 = createFanzoneForNoValidation();
    f5.setName("Invalid");
    f5.setTeamId("1005");
    Fanzone f6 = createFanzoneForNoValidation();
    f6.setName("Invalid2");
    f6.setTeamId("1006");
    Fanzone f7 = createFanzoneForNoValidation();
    f7.setName("Chennai");
    f7.setTeamId("1007");
    fanzoneList.add(f1);
    fanzoneList.add(f2);
    fanzoneList.add(f3);
    fanzoneList.add(f4);
    fanzoneList.add(f5);
    fanzoneList.add(f6);
    fanzoneList.add(f7);
    return fanzoneList;
  }
}
