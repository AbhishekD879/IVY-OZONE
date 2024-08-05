package com.coral.oxygen.middleware.featured.consumer

import com.coral.oxygen.cms.api.CmsService
import com.coral.oxygen.middleware.common.service.AssetManagementService
import com.coral.oxygen.middleware.common.service.featured.IdsCollector
import com.coral.oxygen.middleware.common.service.featured.OddsCardHeader
import com.coral.oxygen.middleware.featured.configuration.FeaturedConfiguration
import com.coral.oxygen.middleware.featured.consumer.sportpage.*
import com.coral.oxygen.middleware.featured.consumer.sportpage.bets.PopularBetModuleProcessor
import com.coral.oxygen.middleware.featured.consumer.sportpage.virtual.VirtualEventsModuleProcessor
import com.coral.oxygen.middleware.featured.service.*
import com.coral.oxygen.middleware.featured.service.injector.*
import com.coral.oxygen.middleware.featured.utils.TestUtils
import com.coral.oxygen.middleware.pojos.model.InPlayTopLevelType
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig
import com.coral.oxygen.middleware.pojos.model.cms.featured.*
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome
import com.coral.oxygen.middleware.pojos.model.output.OutputPrice
import com.coral.oxygen.middleware.pojos.model.output.featured.*
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.Children
import com.egalacoral.spark.siteserver.model.Event
import org.apache.commons.lang3.math.NumberUtils
import org.springframework.test.util.ReflectionTestUtils
import spock.lang.Specification

import java.util.function.Function
import java.util.stream.Collectors

import static com.coral.oxygen.middleware.featured.utils.FeaturedDataUtils.*

class FeaturedDataConsumerSpec extends Specification {

  FeaturedDataConsumer featuredDataConsumer

  CmsService cmsService
  EventDataInjector eventDataInjector
  SingleOutcomeEventsModuleInjector singleOutcomeDataInjector
  RacingEventsModuleInjector racingDataInjector
  MarketsCountInjector marketsCountInjector
  FeaturedCommentaryInjector commentaryInjector
  FeaturedDataFilter featuredDataFilter
  OddsCardHeader oddsCardHeader
  BybService bybService
  HighlightCarouselModuleProcessor highlightCarouselModuleProcessor
  FanzoneHighlightCarouselModuleProcessor fanzoneHighlightCarouselModuleProcessor
  SportPageFilter sportPageFilter
  SurfaceBetModuleProcessor surfaceBetModuleProcessor
  FanzoneSurfaceBetModuleProcessor fanzoneSurfaceBetModuleProcessor
  InplayModuleConsumer inplayModuleConsumer
  SiteServerApi siteServerApi
  FeaturedModuleProcessor featuredModuleProcessor
  AemCarouselsProcessor aemCarouselsProcessor
  QuickLinkModuleProcessor quickLinkModuleProcessor
  FanzoneQuickLinkModuleProcessor fanzoneQuickLinkModuleProcessor
  RacingModuleProcessor racingModuleProcessor
  FeaturedModelStorageService storageService
  FeaturedConfiguration config
  AssetManagementService assetManagementService;
  FeaturedNextRacesConfigProcessor nextRacesConfigProcessor;
  FanBetsFZModuleProcessor fanBetsFZModuleProcessor;
  TeamBetsFZModuleProcessor teamBetsFZModuleProcessor;
  VirtualEventsModuleProcessor virtualEventsModuleProcessor;
  PopularBetModuleProcessor popularBetModuleProcessor
  LuckyDipModuleProcessor luckyDipModuleProcessor

  BybWidgetProcessor bybWidgetProcessor;
  PopularAccaModuleProcessor popularAccaModuleProcessor;

  def setup() {
    cmsService = Mock(CmsService)
    siteServerApi = Mock(SiteServerApi)
    eventDataInjector = Mock(EventDataInjector)
    singleOutcomeDataInjector = Mock(SingleOutcomeEventsModuleInjector)
    racingDataInjector = Mock(RacingEventsModuleInjector)
    marketsCountInjector = Mock(MarketsCountInjector)
    commentaryInjector = Mock(FeaturedCommentaryInjector)
    featuredDataFilter = Mock(FeaturedDataFilter)
    oddsCardHeader = Mock(OddsCardHeader)
    bybService = Mock(BybService)
    highlightCarouselModuleProcessor = Mock(HighlightCarouselModuleProcessor)
    fanzoneHighlightCarouselModuleProcessor=Mock(FanzoneHighlightCarouselModuleProcessor)
    sportPageFilter = Mock(SportPageFilter)
    surfaceBetModuleProcessor = Mock(SurfaceBetModuleProcessor)
    fanzoneSurfaceBetModuleProcessor=Mock(FanzoneSurfaceBetModuleProcessor)
    inplayModuleConsumer = Mock(InplayModuleConsumer)
    featuredModuleProcessor = Mock(FeaturedModuleProcessor)
    aemCarouselsProcessor = Mock(AemCarouselsProcessor)
    quickLinkModuleProcessor = new QuickLinkModuleProcessor()
    fanzoneQuickLinkModuleProcessor = Mock(FanzoneQuickLinkModuleProcessor)
    racingModuleProcessor = Mock(RacingModuleProcessor)
    storageService = Mock(FeaturedModelStorageService)
    assetManagementService = Mock(AssetManagementService);
    nextRacesConfigProcessor = Mock(FeaturedNextRacesConfigProcessor);
    teamBetsFZModuleProcessor = Mock(TeamBetsFZModuleProcessor);
    fanBetsFZModuleProcessor = Mock(FanBetsFZModuleProcessor);
    virtualEventsModuleProcessor = Mock(VirtualEventsModuleProcessor);
    bybWidgetProcessor = Mock(BybWidgetProcessor);
    luckyDipModuleProcessor= Mock(LuckyDipModuleProcessor);
    popularAccaModuleProcessor = Mock(PopularAccaModuleProcessor);

    config = new FeaturedConfiguration(
        eventDataInjector,
        singleOutcomeDataInjector,
        racingDataInjector,
        marketsCountInjector,
        commentaryInjector,
        featuredDataFilter,
        oddsCardHeader,
        bybService,
        cmsService,
        highlightCarouselModuleProcessor,
        fanzoneHighlightCarouselModuleProcessor,
        sportPageFilter,
        surfaceBetModuleProcessor,
        fanzoneSurfaceBetModuleProcessor,
        inplayModuleConsumer,
        featuredModuleProcessor,
        aemCarouselsProcessor,
        quickLinkModuleProcessor,
        fanzoneQuickLinkModuleProcessor,
        racingModuleProcessor,
        storageService,
        assetManagementService,
        nextRacesConfigProcessor,
        teamBetsFZModuleProcessor,
        fanBetsFZModuleProcessor,
        virtualEventsModuleProcessor,
        popularBetModuleProcessor,
        bybWidgetProcessor,
        luckyDipModuleProcessor,
        popularAccaModuleProcessor
        )
    featuredDataConsumer = new FeaturedDataConsumer(config)
    featuredDataConsumer.setFanzonePageId("160")
    featuredModuleProcessor.getFirstFeaturedEventModules(*_) >> { SportModule cmsModule, ModularContent modularContent, Set<Long> excludedEventIds ->
      toFeaturedModule(cmsModule, modularContent)
    }

    inplayModuleConsumer.processSegmentwiseModules(*_) >> {InplayModule module, Map<String, SegmentView> segmentWiseModules, String inplayModule ->
      createSegmentWiseModules(module,segmentWiseModules)
    }
  }

  private ModularContentItem prepareConsumerTestMock(FeaturedRawIndex.PageType pageType) throws IOException {
    // prepare data from CMS
    ModularContent modularContent =
        getModularContentFromResource('featured_consumption_cms_modular_content_output.json')
    ModularContentItem item = prepareModularContentItem(modularContent)
    List<SportsQuickLink> cmsQuickLinks = getCmsQuickLinksFromResource('featured_consumption_cms_quick_links_output.json')
    InPlayConfig cmsInPlayConfig = TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/cmsConfigWithSegments.json",
        InPlayConfig.class)
    SportPageModule featuredModule = createModule(0, 0, ModuleType.FEATURED, modularContent, pageType)
    SportPageModule quickLinkModule = createModule(0, 0, ModuleType.QUICK_LINK, cmsQuickLinks, pageType)
    SportPageModule inplayModule = createModule(0, 0, ModuleType.INPLAY, Arrays.asList(cmsInPlayConfig), pageType)
    def sportPages = Collections.singletonList(new SportPage('0', Arrays.asList(featuredModule,inplayModule, quickLinkModule)))
    CmsSystemConfig cmsSystemConfig1 = new CmsSystemConfig();

    storageService.getLastRunTime() >> null
    cmsService.requestModularContent() >> modularContent
    cmsService.requestPages() >> sportPages
    cmsService.requestSystemConfig() >> cmsSystemConfig1
    cmsService.requestSportsQuickLink() >> cmsQuickLinks
    sportPageFilter.isSupportedPage(*_) >> true
    inplayModuleConsumer.processModule(*_) >> {SportPageModule cmsInplayModule, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds ->
      createInplayModule(pageType)
    }

    return item
  }

  private static ModularContentItem prepareModularContentItem(ModularContent modularContent) {
    ModularContentItem item = modularContent.stream()
        .filter({ element -> 'featured'.equalsIgnoreCase(element.getDirectiveName()) })
        .findFirst()
        .get()
    item.getModules()
        .get(1)
        .getData()
    //        .add(null)
    item.setModules(Arrays.asList(item.getModules().get(0), item.getModules().get(1)))

    return item
  }

  def "Test setting enhanced/special from 'badge' field for OutputModules"() throws Exception {
    ModularContent modularContent = getModularContentFromResource('modular_content.json')
    SportModule sportModule = new SportModule()

    when:
    ModularContentItem modularContentItem =
        modularContent.stream().filter({ item -> 'featured'.equalsIgnoreCase(item.getDirectiveName()) })
        .findFirst()
        .get()
    EventsModule outputModule0 = new EventsModule(sportModule, modularContentItem.getModules().get(0))
    EventsModule outputModule1 = new EventsModule(sportModule, modularContentItem.getModules().get(1))
    EventsModule outputModule2 = new EventsModule(sportModule, modularContentItem.getModules().get(2))
    EventsModule outputModule3 = new EventsModule(sportModule, modularContentItem.getModules().get(3))
    EventsModule outputModule4 = new EventsModule(sportModule, modularContentItem.getModules().get(4))

    then:
    !outputModule0.getEnhanced()
    !outputModule0.getSpecial()
    outputModule1.getEnhanced()
    !outputModule1.getSpecial()
    !outputModule2.getEnhanced()
    outputModule2.getSpecial()
    outputModule3.getEnhanced()
    outputModule3.getSpecial()
    !outputModule4.getEnhanced()
    !outputModule4.getSpecial()
  }

  def "Calculating outcome columns headers should pass w/o exceptions if no modules present"() {
    when:
    featuredDataConsumer.calculateOutcomeCoulumnsHeaders(Collections.emptyList())

    then:
    0 * oddsCardHeader.calculateHeadTitles(_)
    noExceptionThrown()
  }

  def "Check consumeInParallels result"() throws Exception {
    ModularContentItem item = prepareConsumerTestMock(FeaturedRawIndex.PageType.sport)

    when:
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels()

    then:
    data != null
    List<FeaturedModel> resultList = data.getFeaturedModels()
    resultList != null
    resultList.size() == 1
    def result = resultList.get(0)
    result.getTitle() == '0 sport page'
    result.getShowTabOn() == item.getShowTabOn()
    result.getDirectiveName() == 'sport'
    result.isVisible() == item.isVisible()
    result.getModules().size() == 4
    result.getModules()
        .stream()
        .filter({ outputModule -> outputModule.isErrorEmpty() })
        .count() == 4
    def cashoutList = result.getModules()
        .stream()
        .filter({ module -> module.getModuleType() == ModuleType.FEATURED })
        .map({ eventsModule -> eventsModule.getCashoutAvail() })
        .collect(Collectors.toList())

    def quickLinkModule = result.getModules()
        .stream()
        .filter({ module -> module.getModuleType() == ModuleType.QUICK_LINK })
        .findFirst()

    quickLinkModule.isPresent()
    quickLinkModule.get().getSportId() == 0
    quickLinkModule.get().getData().size() == 9

    //cashoutList.contains(true) || cashoutList.contains(false)
  }

  def "Check modules ordered"() throws Exception {
    given:

    def sportPages = getCmsSportPagesFromResource('featured_consumption_cms_sportPages_output.json')
    highlightCarouselModuleProcessor.processModules(*_) >>
    { SportPageModule carousel, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds -> toHighlightCarouseFeatureModule(carousel) }

    and:
    storageService.getLastRunTime() >> null
    cmsService.requestPages() >> sportPages
    cmsService.requestSystemConfig() >> new CmsSystemConfig()
    sportPageFilter.isSupportedPage(*_) >> true

    when:
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels()

    then:
    data != null
    List<FeaturedModel> resultList = data.getFeaturedModels()
    resultList != null
    resultList.size() == 1
    def result = resultList.get(0)
    result.getModules().size() == 6
    checkModulesOrdered(result.getModules())
  }

  def toHighlightCarouseFeatureModule(SportPageModule sportPageModule) {
    SportModule cmsSportModule = sportPageModule.getSportModule()
    List<HighlightCarouselModule> modules = new ArrayList<>()
    for (SportPageModuleDataItem pageModel : sportPageModule.getPageData()) {
      HighlightCarousel carousel = (HighlightCarousel) pageModel
      HighlightCarouselModule module = new HighlightCarouselModule()
      module.setLimit(carousel.getLimit())
      module.setTitle(carousel.getTitle())
      module.setDisplayOrder(cmsSportModule.getSortOrderOrDefault(null))
      module.setSecondaryDisplayOrder(carousel.getDisplayOrder() == null ? BigDecimal.ZERO : BigDecimal.valueOf(carousel.getDisplayOrder()))

      module.setData(carousel.getEvents().stream().map(createEvent()).collect(Collectors.toList()))
      modules.add(module)
    }
    modules
  }

  def toFeaturedModule(SportModule cmsSportModule, ModularContent modularContent) {
    ModularContentItem modularContentItem = modularContent.stream()
        .filter { item -> 'featured'.equalsIgnoreCase(item.getDirectiveName()) }
        .findFirst().orElse(null)
    return modularContentItem.getModules().stream()
        .map { module -> new EventsModule(cmsSportModule, module) }
        .collect(Collectors.toList())
  }

  Function<String, EventsModuleData> createEvent() {
    new Function<String, EventsModuleData>() {

          @Override
          EventsModuleData apply(String eventId) {
            EventsModuleData eventsModuleData = new EventsModuleData()
            eventsModuleData.setId(NumberUtils.toLong(eventId))
            eventsModuleData.setTypeId('12')
            return eventsModuleData
          }
        }
  }

  boolean checkModulesOrdered(List<AbstractFeaturedModule> modules) {
    if (modules.size() <= 1) {
      return true
    }
    def displayOrder = modules.get(0).getDisplayOrder()
    def secondaryDisplayOrder = modules.get(0).getSecondaryDisplayOrder()
    for (def i = 0; i < modules.size(); i++) {
      if (modules.get(i).getDisplayOrder() == null) {
        for (def j = i; j < modules.size(); j++) {
          if (modules.get(i).getDisplayOrder() != null) {
            // NULLs should be last
            return false
          }
        }
        break
      }
      if (modules.get(i).getDisplayOrder() < displayOrder) {
        return false
      }
      if (modules.get(i).getDisplayOrder() == displayOrder) {
        if (modules.get(i).getSecondaryDisplayOrder() != null && (secondaryDisplayOrder == null || modules.get(i).getSecondaryDisplayOrder() < secondaryDisplayOrder)) {
          return false
        }
      }
      displayOrder = modules.get(i).getDisplayOrder()
      secondaryDisplayOrder = modules.get(i).getSecondaryDisplayOrder()
    }
    true
  }

  Children createEventChildren(String eventId, String eventName) {
    def event = new Event()
    event.id = eventId
    event.typeId = '2'
    event.name = eventName

    def child = new Children()
    child.event = event
    child
  }

  private static SportPageModule createModule(Integer sportId, double sortOrder, ModuleType moduleType, List<? extends SportPageModuleDataItem> moduleData, FeaturedRawIndex.PageType pageType) {
    def module = new SportModule()
    module.sportId = sportId
    module.setModuleType(moduleType)
    module.setSortOrder(sortOrder)
    module.setPageType(pageType)
    new SportPageModule(module, moduleData)
  }

  def "Check consumeInParallels result with Quick Links returned"() throws Exception {
    ModularContentItem item = prepareConsumerTestMock(FeaturedRawIndex.PageType.sport)

    when:
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels()

    then:
    data != null
    List<FeaturedModel> resultList = data.getFeaturedModels()
    resultList != null
    resultList.size() == 1
    def result = resultList.get(0)
    result.getTitle() == '0 sport page'
    result.getShowTabOn() == item.getShowTabOn()
    result.getDirectiveName() == 'sport'
    result.isVisible() == item.isVisible()
    result.getModules().size() == 4
    result.getModules()
        .stream()
        .filter({ outputModule -> outputModule.isErrorEmpty() })
        .count() == 4
    def cashoutList = result.getModules()
        .stream()
        .filter({ module -> module.getModuleType() == ModuleType.FEATURED })
        .map({ eventsModule -> eventsModule.getCashoutAvail() })
        .collect(Collectors.toList())

    //cashoutList.contains(true) || cashoutList.contains(false)
  }

  def "Check consumeInParallels for eventhubs"() throws Exception {
    ModularContentItem item = prepareConsumerTestMock(FeaturedRawIndex.PageType.eventhub)

    when:
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels()

    then:
    data != null
    !data.getSportPages().isEmpty()
    List<FeaturedModel> resultList = data.getFeaturedModels()
    resultList != null
    resultList.size() == 1
    def result = resultList.get(0)
    result.getTitle() == '0 sport page'
    result.getShowTabOn() == item.getShowTabOn()
    result.getDirectiveName() == 'sport'
    result.isVisible() == item.isVisible()
    result.getModules().size() == 4
    def module = result.getModules().get(0)
    module.getPageType() == FeaturedRawIndex.PageType.eventhub
  }

  def "Check consumeInParallels no data from cms"() throws Exception {
    storageService.getLastRunTime() >> null
    cmsService.requestPages() >> Collections.emptyList()

    when:
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels()

    then:
    data != null
    data.getFeaturedModels().isEmpty()
    data.getSportPages().isEmpty()
  }

  def "Check ConsumeInParallels HCEventIdsCMSOrder should not be sorted"(){
    given:
    highlightCarouselModuleProcessor=new HighlightCarouselModuleProcessor(siteServerApi, eventDataInjector, marketsCountInjector, commentaryInjector)
    ReflectionTestUtils.setField(config,"highlightCarouselModuleProcessor",highlightCarouselModuleProcessor)
    featuredDataConsumer = config.createFeaturedDataConsumer()

    def sportPageHC =getCmsSportPagesFromResource("featured_eventhub_cms_highlights_carousel_output.json")
    def inputHC = (HighlightCarousel) sportPageHC.get(0).getSportPageModules().get(0).getPageData().get(0)
    inputHC.displayMarketType="Primary"
    def inputHCEventIds = inputHC.getEvents().stream().map(Long.&parseLong).collect(Collectors.toList())
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig();

    storageService.getLastRunTime() >> null
    cmsService.requestPages() >> sportPageHC
    cmsService.requestSystemConfig() >> cmsSystemConfig
    sportPageFilter.isSupportedPage(*_) >> true

    siteServerApi.getEventToOutcomeForEvent(*_) >>
        Optional.of(Arrays.asList("10578421", "10579407").stream()
        .map({ id ->
          def event = new Event(); event.id = id
          def che = new Children(); che.event = event; che
        })
        .collect()
        )

    siteServerApi.getEventForType(*_) >> Optional.of(
        Collections.singletonList("3437").stream()
        .map({ id -> def event = new Event(); event.id = id; event })
        .collect()
        )

    eventDataInjector.injectData(_ as List<EventsModuleData>, _ as IdsCollector,"Primary" as String) >> { arguments ->
      (arguments[0] as List)
          .forEach { event ->
            def outcome = new OutputOutcome()
            outcome.setPrices(Collections.singletonList(new OutputPrice()))
            def market = new OutputMarket()
            market.setOutcomes(Collections.singletonList(outcome))
            (event as EventsModuleData).markets = Collections.singletonList(market)
            (event as EventsModuleData).typeId = "442"
          }
    }

    when:
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels()
    def outputHCEventIds = ((HighlightCarouselModule) data.getFeaturedModels().get(0).getModules().get(0)).getEventIds()

    then:
    inputHCEventIds == outputHCEventIds
  }

  def "Check ConsumeInParallels segmented HCEventIdsCMSOrder should not be sorted"(){
    given:
    highlightCarouselModuleProcessor=new HighlightCarouselModuleProcessor(siteServerApi, eventDataInjector, marketsCountInjector, commentaryInjector)
    ReflectionTestUtils.setField(config,"highlightCarouselModuleProcessor",highlightCarouselModuleProcessor)
    featuredDataConsumer = config.createFeaturedDataConsumer()

    def sportPageHC =getCmsSportPagesFromResource("featured_eventhub_cms_highlights_carousel_output.json")
    def inputHC = (HighlightCarousel) sportPageHC.get(0).getSportPageModules().get(0).getPageData().get(0)
    inputHC.displayMarketType="Primary"
    def inputHCEventIds = inputHC.getEvents().stream().map(Long.&parseLong).collect(Collectors.toList())

    InPlayConfig cmsInPlayConfig = TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/cmsConfigWithSegments.json",
        InPlayConfig.class)
    SportPageModule inplayModule = createModule(0, 0, ModuleType.INPLAY, Arrays.asList(cmsInPlayConfig), FeaturedRawIndex.PageType.sport)
    sportPageHC.get(0).getSportPageModules().add(inplayModule)
    sportPageHC.get(0).setSegmented(true)
    CmsSystemConfig cmsSystemConfig1 = new CmsSystemConfig();

    storageService.getLastRunTime() >> null
    cmsService.requestPages() >> sportPageHC
    cmsService.requestSystemConfig() >> cmsSystemConfig1
    sportPageFilter.isSupportedPage(*_) >> true

    inplayModuleConsumer.processModule(*_) >> {SportPageModule cmsInplayModule, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds ->
      createInplayModule(FeaturedRawIndex.PageType.sport)
    }

    siteServerApi.getEventToOutcomeForEvent(*_) >>
        Optional.of(Arrays.asList("10578421", "10579407").stream()
        .map({ id ->
          def event = new Event(); event.id = id
          def che = new Children(); che.event = event; che
        })
        .collect()
        )

    siteServerApi.getEventForType(*_) >> Optional.of(
        Collections.singletonList("3437").stream()
        .map({ id -> def event = new Event(); event.id = id; event })
        .collect()
        )

    eventDataInjector.injectData(_ as List<EventsModuleData>, _ as IdsCollector,"Primary" as String) >> { arguments ->
      (arguments[0] as List)
          .forEach { event ->
            def outcome = new OutputOutcome()
            outcome.setPrices(Collections.singletonList(new OutputPrice()))
            def market = new OutputMarket()
            market.setOutcomes(Collections.singletonList(outcome))
            (event as EventsModuleData).markets = Collections.singletonList(market)
            (event as EventsModuleData).typeId = "442"
          }
    }

    when:
    FeaturedModelsData data = featuredDataConsumer.consumeInParallels()
    def outputHCEventIds = ((HighlightCarouselModule) data.getFeaturedModels().get(0).getModules().get(0)).getEventIds()

    then:
    inputHCEventIds == outputHCEventIds
  }

  private static ModularContent getModularContentFromResource(String resource) throws IOException {
    List<ModularContentItem> items = getModularContentItemsFromResource(resource)
    ModularContent modularContent = new ModularContent()
    modularContent.addAll(items)
    return modularContent
  }

  private AbstractFeaturedModule<?> createInplayModule(FeaturedRawIndex.PageType pageType) {

    InplayModule inplayModule = new InplayModule();
    inplayModule.setTotalEvents(10);
    updateAbstractFeaturedModule(inplayModule, "@InplayModule","InplayModule", pageType);
    SportSegment segmentdata = new SportSegment();
    List<SportSegment> sportSegList = new ArrayList<>();
    segmentdata.setCategoryId(20);
    segmentdata.setShowInPlay(true);
    segmentdata.setCategoryName("categoryName");
    segmentdata.setCategoryCode("CatCode");
    segmentdata.setCategoryPath("path");
    segmentdata.setDisplayOrder(10);
    segmentdata.setSportUri("sporturi");
    segmentdata.setSvgId("svgid");
    segmentdata.setEventCount(10);
    segmentdata.setMarketSelector("MarketSelector");
    segmentdata.setTopLevelType(InPlayTopLevelType.UPCOMING_EVENT);
    segmentdata.setMarketSelectorOptions(Arrays.asList("213,345,678".split(",")));
    Collection<Long> eventsIds = new ArrayList<>();
    eventsIds.add(10579407);
    segmentdata.setEventsIds(eventsIds);
    segmentdata.setSegments(Arrays.asList("s1,Universal".split(",")));
    List<SegmentReference> segmentReferences = new ArrayList<>();
    SegmentReference reference = new SegmentReference();
    reference.setSegment("s1");
    reference.setDisplayOrder(20.0);
    segmentReferences.add(reference);
    segmentdata.setSegmentReferences(segmentReferences);

    TypeSegment segment = new TypeSegment();
    List<TypeSegment> segments = new ArrayList<>();
    EventsModuleData eventsModuleData = new EventsModuleData();
    eventsModuleData.setId(10001);
    List<EventsModuleData> events = new ArrayList<>();
    events.add(eventsModuleData);

    segment.setClassName("className");
    segment.setCategoryName("categoryname");
    segment.setCategoryCode("categoryCode");
    segment.setTypeName("typename");
    segment.setTypeId("Typeid");
    segment.setClassDisplayOrder(10);
    segment.setTypeDisplayOrder(10);
    segment.setTypeSectionTitleAllSports("sports");
    segment.setTypeSectionTitleOneSport("sports");
    segment.setTypeSectionTitleConnectApp("connectapps");
    segment.setEventCount(10);
    segment.setEventsIds(new ArrayList<>());
    segment.setEvents(events);
    segments.add(segment);
    segmentdata.setEventsByTypeName(segments);
    sportSegList.add(segmentdata);

    inplayModule.setData(sportSegList);

    return inplayModule;
  }

  private void updateAbstractFeaturedModule(
      AbstractFeaturedModule featureModule, String id,String title, FeaturedRawIndex.PageType pageType) {
    if (id == null) {
      featureModule.setId("1213");
    } else {
      featureModule.setId(id);
    }
    featureModule.setPageType(pageType);
    featureModule.setSportId(0);
    featureModule.setTitle(title);
    featureModule.setDisplayOrder(BigDecimal.ZERO);
    featureModule.setSecondaryDisplayOrder(BigDecimal.ZERO);
    featureModule.setSortOrder(0.0);
    featureModule.setSegmented(true);
    featureModule.setShowExpanded(true);
    featureModule.setPublishedDevices(Arrays.asList("desktop,tablet,mobile1".split(",")));
  }
  private void createSegmentWiseModules(InplayModule module,Map<String, SegmentView> segmentWiseModules) {

    SegmentView segmentView = new SegmentView()
    SegmentOrderdModuleData segmentOrderdModuleForQl = new SegmentOrderdModuleData(1, module.getData().get(0))
    segmentView.getInplayModuleData().put(module.getId(), segmentOrderdModuleForQl)
    segmentWiseModules.put("Universal", segmentView)
    segmentWiseModules.put("s1", segmentView)
    SegmentView segmentView1 = new SegmentView()
    SegmentOrderdModuleData segmentOrderdModuleForQ2 = new SegmentOrderdModuleData(2, module.getData().get(0))
    List<Long> eventIds = new ArrayList<>()
    eventIds.add(123)
    segmentOrderdModuleForQ2.setEventIds(eventIds)
    segmentView1.getInplayModuleData().put(module.getId(), segmentOrderdModuleForQ2)
    segmentWiseModules.put("s2", segmentView1)
  }
}
