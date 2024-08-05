package com.coral.oxygen.middleware.featured.service;

import com.coral.oxygen.middleware.pojos.model.InPlayTopLevelType;
import com.coral.oxygen.middleware.pojos.model.cms.ModuleDataSelection;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SegmentReference;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.output.*;
import com.coral.oxygen.middleware.pojos.model.output.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.time.Instant;
import java.util.*;
import lombok.NoArgsConstructor;

@NoArgsConstructor
public class FaeturemodelUtil {

  private FeaturedModel model;

  public FeaturedModel creatFeatureModel(boolean isinvalidate) {
    model = new FeaturedModel();
    model.setDirectiveName("HighLightTab");
    model.setPageId("0");
    model.setVisible(true);
    model.setFeatureStructureChanged(true);
    model.setSegmented(true);

    ArrayList<AbstractFeaturedModule<?>> modules = new ArrayList<>();
    modules.add(createSufaceBetModule(isinvalidate));
    modules.add(createQuickLinkModule(isinvalidate));
    modules.add(createHighlightCarouselModule());
    modules.add(CreateEventModules());
    modules.add(createInplayModule());
    modules.add(createAemBannersModule());
    modules.add(createRecentlyPlayedGameModule());
    modules.add(createRacingModule());
    modules.add(createVirtualRaceModuleData());
    modules.add(createRacingEventsModule());
    modules.add(createHighlightCarouselModuleWih2UpMarket());

    model.setModules(modules);
    return model;
  }

  public FeaturedModel createStructureWithSegmentWiseModules(String pageId) {
    FeaturedModel model = new FeaturedModel();

    List<AbstractFeaturedModule<?>> modules = new ArrayList<>();
    model.setPageId(pageId);
    Map<String, SegmentView> segmentWiseModules = new HashMap<>();
    SegmentView segmentView = new SegmentView();
    HighlightCarouselModule highlightCarouselModule =
        (HighlightCarouselModule) createHighlightCarouselModule();
    modules.add(highlightCarouselModule);
    SegmentOrderdModule segmentOrderdModuleForHc =
        new SegmentOrderdModule(1, highlightCarouselModule);
    segmentView
        .getHighlightCarouselModules()
        .put(highlightCarouselModule.getId(), segmentOrderdModuleForHc);

    EventsModule featureModule = (EventsModule) CreateEventModules();
    modules.add(featureModule);
    SegmentOrderdModule segmentOrderdModuleForEventModule =
        new SegmentOrderdModule(1, featureModule);
    segmentView.getEventModules().put(featureModule.getId(), segmentOrderdModuleForEventModule);

    QuickLinkModule quickLinkModule = (QuickLinkModule) createQuickLinkModule(false);
    modules.add(quickLinkModule);
    model.setQuickLinkModule(quickLinkModule);
    SegmentOrderdModuleData segmentOrderdModuleForQl =
        new SegmentOrderdModuleData(1, quickLinkModule.getData().get(0));
    segmentView.getQuickLinkData().put(quickLinkModule.getId(), segmentOrderdModuleForQl);

    SurfaceBetModule surfaceBetModule = (SurfaceBetModule) createSufaceBetModule(false);
    modules.add(surfaceBetModule);
    model.setSurfaceBetModule(surfaceBetModule);
    SegmentOrderdModuleData segmentOrderdModuleForSb =
        new SegmentOrderdModuleData(1, surfaceBetModule.getData().get(0));
    segmentView.getSurfaceBetModuleData().put(surfaceBetModule.getId(), segmentOrderdModuleForSb);

    InplayModule inplayModule = (InplayModule) createInplayModule();
    modules.add(inplayModule);
    model.setInplayModule(inplayModule);
    SegmentOrderdModuleData segmentOrderdModuleForInplay =
        new SegmentOrderdModuleData(1, inplayModule.getData().get(0));
    List<SegmentedEvents> limitedEvents = new ArrayList<>();
    SegmentedEvents segmentedEvents = new SegmentedEvents();
    TypeSegment eventByTypeName = new TypeSegment();
    EventsModuleData eventsModuleData = new EventsModuleData();
    List<EventsModuleData> events = new ArrayList<>();
    events.add(eventsModuleData);
    segmentedEvents.setEventByTypeName(eventByTypeName);
    segmentedEvents.setEvents(events);
    limitedEvents.add(segmentedEvents);
    segmentOrderdModuleForInplay.setLimitedEvents(limitedEvents);
    segmentView.getInplayModuleData().put(inplayModule.getId(), segmentOrderdModuleForInplay);

    segmentWiseModules.put("Universal", segmentView);
    segmentWiseModules.put("segment-one", segmentView);
    model.setSegmentWiseModules(segmentWiseModules);

    model.setModules(modules);
    return model;
  }

  private AbstractFeaturedModule<?> createRacingEventsModule() {
    RacingEventsModule racingEventsModule =
        new RacingEventsModule(createsportsModule("RacingEventsModule"), "Horse", true);
    racingEventsModule.setModuleType(ModuleType.RACING_EVENT_MODULE);
    updateAbstractFeaturedModule(racingEventsModule, "@RacingModule", "RacingModule");
    RacingEventData racingEventData = new RacingEventData();
    List<RacingEventData> racingEventDatas = new ArrayList<>();

    racingEventData.setCategoryId("CategoryId");
    racingEventData.setCategoryName("categoryName");
    racingEventData.setClassId("classId");
    racingEventData.setClassName("classname");
    racingEventData.setTypeName("typename");
    racingEventData.setCashoutAvail("avail");
    racingEventData.setDisplayOrder(10);
    racingEventData.setClassDisplayOrder(10);
    racingEventData.setTypeDisplayOrder(10);
    racingEventData.setIsStarted(true);
    racingEventData.setIsLiveNowEvent(true);
    racingEventData.setIsFinished(true);
    racingEventData.setIsResulted(true);
    racingEventData.setRawIsOffCode("raw");
    racingEventData.setTypeFlagCodes("flagCode");
    racingEventData.setDrilldownTagNames("tagnemae");
    racingEventData.setPoolTypes(Arrays.asList("1,2,45,6".split(",")));
    racingEventData.setMarkets(new ArrayList<>());
    racingEventDatas.add(racingEventData);
    racingEventsModule.setData(racingEventDatas);
    return racingEventsModule;
  }

  private VirtualRaceModule createVirtualRaceModuleData() {
    VirtualRaceModule virtualRaceModule =
        new VirtualRaceModule(createsportsModule("VirtualRacingEventsModule"), true);
    updateAbstractFeaturedModule(virtualRaceModule, "@virtualRaceModule", "virtualRaceModule");
    VirtualRaceModuleData moduledate = new VirtualRaceModuleData();
    List<VirtualRaceModuleData> moduleDatas = new ArrayList<>();

    moduledate.setClassId("classId");
    updateBasicRacingEventData(moduledate, "virtualRaceModule");
    moduleDatas.add(moduledate);
    virtualRaceModule.setData(moduleDatas);
    return virtualRaceModule;
  }

  private AbstractFeaturedModule<?> createRacingModule() {
    RacingModule racingModule = new RacingModule();
    updateAbstractFeaturedModule(racingModule, "@RacingModule", "RacingModule");
    RacingModuleConfig racingModuleConfig = new RacingModuleConfig();
    List<RacingModuleConfig> configlist = new ArrayList<>();
    racingModuleConfig.setId("xacewe12121ndsndf");
    racingModuleConfig.setName("RacingModule");
    racingModuleConfig.setActive(true);
    racingModuleConfig.setGuid("0ewe2322121321");
    configlist.add(racingModuleConfig);
    racingModule.setData(configlist);
    return racingModule;
  }

  private AbstractFeaturedModule<?> createAemBannersModule() {
    AemBannersModule aemBannersModule = new AemBannersModule();
    aemBannersModule.setModuleType(ModuleType.AEM_BANNERS);
    updateAbstractFeaturedModule(aemBannersModule, "@aemBannersModule", "aemBannersModule");
    AemBannersImg aemdata = new AemBannersImg();
    List<AemBannersImg> imgList = new ArrayList<>();
    aemdata.setOfferTitle("offertirle");
    aemdata.setOfferName("offername");
    aemdata.setImgUrl("image");
    aemdata.setWebUrl("weburl");
    aemdata.setRoxanneWebUrl("roxennaurl");
    aemdata.setAppUrl("appurl");
    aemdata.setRoxanneAppUrl("apprurl");
    aemdata.setWebTarget("target");
    aemdata.setAppTarget("target");
    aemdata.setSelectionId("selectionId");
    aemdata.setAltText("text");
    aemdata.setWebTandC("webTandC");
    aemdata.setWebTandCLink("webTandC");
    aemdata.setMobTandCLink("MobTandCLink");
    aemdata.setIsScrbrd("scoreboard");
    aemdata.setScrbrdEventId("eventid");
    aemdata.setScrbrdPosition("position");
    aemdata.setScrbrdTypeId("typeId");
    aemdata.setDisplayOrder(10);
    aemdata.setImsLevel(new HashSet<>(Arrays.asList("1,2,45,6".split(","))));
    aemdata.setUserType(new HashSet<>(Arrays.asList("MUSER,DUSER,TUSER".split(","))));
    aemdata.setSelectChannels(new HashSet<>(Arrays.asList("MOBILE,DESKTOP,TABLET".split(","))));
    aemdata.setGuid("0ewe2322121321");
    imgList.add(aemdata);
    aemBannersModule.setData(imgList);

    return aemBannersModule;
  }

  private AbstractFeaturedModule<?> createRecentlyPlayedGameModule() {

    RecentlyPlayedGameModule recentlyPlayedGameModule = new RecentlyPlayedGameModule();
    recentlyPlayedGameModule.setModuleType(ModuleType.RECENTLY_PLAYED_GAMES);
    updateAbstractFeaturedModule(
        recentlyPlayedGameModule, "@recentlyPlayedGameModule", "recentlyPlayedGameModule");
    RpgConfig config = new RpgConfig();
    List<RpgConfig> configlist = new ArrayList<>();
    config.setTitle("recentlyPlayedGameModule");
    config.setSeeMoreLink("HTTP://GOOGLE.COM");
    config.setBundleUrl("HTTP://GOOGLE.COM");
    config.setLoaderUrl("HTTP://GOOGLE.COM");
    config.setGamesAmount(10);
    configlist.add(config);
    recentlyPlayedGameModule.setData(configlist);
    return recentlyPlayedGameModule;
  }

  private AbstractFeaturedModule<?> createInplayModule() {

    InplayModule inplayModule = new InplayModule();
    inplayModule.setTotalEvents(10);
    updateAbstractFeaturedModule(inplayModule, "@InplayModule", "InplayModule");
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
    eventsIds.add(100L);
    segmentdata.setEventsIds(eventsIds);

    TypeSegment segment = new TypeSegment();
    List<TypeSegment> segments = new ArrayList<>();

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
    List<EventsModuleData> moduledataList = new ArrayList<>();
    EventsModuleData moduleDta = new EventsModuleData();
    updateEventsModuleData(moduleDta, "Eventmoduledata");
    moduledataList.add(moduleDta);
    segment.setEvents(moduledataList);
    segments.add(segment);
    segmentdata.setEventsByTypeName(segments);
    segmentdata.setSegments(Arrays.asList("s1".split(",")));
    sportSegList.add(segmentdata);

    inplayModule.setData(sportSegList);

    return inplayModule;
  }

  private AbstractFeaturedModule<?> CreateEventModules() {

    EventsModule module = new EventsModule();
    updateEventModule(module, ModuleType.FEATURED);
    updateSegmentReferences(module, "eventsModule");
    updateAbstractFeaturedModule(module, "@EventModule", "eventsModule");
    EventsModuleData moduleDta = new EventsModuleData();
    List<EventsModuleData> moduledataList = new ArrayList<>();
    updateEventsModuleData(moduleDta, "Eventmoduledata");

    moduledataList.add(moduleDta);
    module.setData(moduledataList);
    return module;
  }

  private AbstractFeaturedModule<?> createHighlightCarouselModule() {
    HighlightCarouselModule module = new HighlightCarouselModule();
    List<Long> eventIds = new ArrayList<>();
    eventIds.add(121L);
    module.setSvgId("svgId");
    module.setLimit(10);
    module.setInPlay(true);
    module.setTypeId(1);
    module.setEventIds(eventIds);
    updateEventModule(module, ModuleType.HIGHLIGHTS_CAROUSEL);
    updateSegmentReferences(module, "HighlightCarousel");
    updateAbstractFeaturedModule(module, "@HighlightCarousel", "HighlightCarousel");
    EventsModuleData moduleDta = new EventsModuleData();
    List<EventsModuleData> moduledataList = new ArrayList<>();
    updateEventsModuleData(moduleDta, "Eventmoduledata");

    moduledataList.add(moduleDta);
    module.setData(moduledataList);
    return module;
  }

  private AbstractFeaturedModule<?> createHighlightCarouselModuleWih2UpMarket() {
    HighlightCarouselModule module = new HighlightCarouselModule();
    List<Long> eventIds = new ArrayList<>();
    eventIds.add(121L);
    module.setSvgId("svgId");
    module.setLimit(10);
    module.setInPlay(true);
    module.setTypeId(12);
    module.setEventIds(eventIds);
    module.setDisplayMarketType("2UpMarket");
    updateEventModule(module, ModuleType.HIGHLIGHTS_CAROUSEL);
    updateSegmentReferences(module, "HighlightCarousel");
    updateAbstractFeaturedModule(module, "@HighlightCarousel", "HighlightCarousel");
    module.setId("12345678");
    EventsModuleData moduleDta = new EventsModuleData();
    List<EventsModuleData> moduledataList = new ArrayList<>();
    updateEventsModuleData(moduleDta, "Eventmoduledata");

    moduledataList.add(moduleDta);
    module.setData(moduledataList);
    module.getData().get(0).getMarkets().get(0).setName("TwoUp");
    return module;
  }

  private AbstractFeaturedModule<?> createQuickLinkModule(boolean isinvalidate) {
    QuickLinkModule module = new QuickLinkModule();
    module.setModuleSegmentView(prepareModuleDataSegmentView("QuickLink"));
    if (isinvalidate) {
      updateAbstractFeaturedModule(module, null, "QuickLink");
    } else {
      updateAbstractFeaturedModule(module, "@QuicklinkModule", "QuickLink");
    }
    QuickLinkData moduledata = new QuickLinkData();
    List<QuickLinkData> moduledatas = new ArrayList<>();

    moduledata.setId("abd031def0313d10212");
    moduledata.setDestination("setDestination");
    moduledata.setSvgId("svgid");
    moduledata.setDisplayOrder(10);
    moduledata.setTitle("title");
    moduledata.setGuid("guid");

    moduledatas.add(moduledata);
    module.setData(moduledatas);
    return module;
  }

  private AbstractFeaturedModule<?> createSufaceBetModule(boolean isinvalidate) {
    SurfaceBetModule module = new SurfaceBetModule();
    module.setMaxRows(5);
    module.setMaxSelections(5);
    module.setYourCallAvailable(true);
    module.setTotalEvents(5);
    module.setOutcomeColumnsTitles(new ArrayList<>());
    module.setShowExpanded(false);
    module.setModuleSegmentView(prepareModuleDataSegmentView("SurfaceBet"));
    if (isinvalidate) {
      updateAbstractFeaturedModule(module, null, "SurfaceBet");
    } else {
      updateAbstractFeaturedModule(module, "@SurfaceBet", "SurfaceBet");
    }
    module.setData(createSurfaceModuledata(isinvalidate));

    return module;
  }

  public List<SurfaceBetModuleData> createSurfaceModuledata(boolean isinvalidate) {

    SurfaceBetModuleData moduledate = new SurfaceBetModuleData();
    List<SurfaceBetModuleData> listModules = new ArrayList<>();
    moduledate.setOldPrice(prepareOutputPrice());
    moduledate.setTitle("SurfaceBetModule");
    moduledate.setContent("surfaceContent");
    moduledate.setSvgId("id");
    moduledate.setSelectionId(BigInteger.valueOf(10));
    moduledate.setObjId("q09olki87jh7171771");
    moduledate.setTypeId("type");
    moduledate.setSvgBgId("Image1");
    moduledate.setSvgBgImgPath("image1");
    moduledate.setContentHeader("Content Header");
    updateEventsModuleData(moduledate, "surfacebetmoduledata");
    if (isinvalidate) {
      moduledate.setObjId(null);
    }
    listModules.add(moduledate);
    return listModules;
  }

  public SportModule createsportsModule(String name) {

    SportModule cmsModule = new SportModule();
    cmsModule.setId("0o313nn3213213d");
    cmsModule.setSportId(16);
    cmsModule.setTitle(name);
    cmsModule.setPublishedDevices(Arrays.asList("desktop,tablet,mobile".split(",")));

    cmsModule.setPageType(FeaturedRawIndex.PageType.sport);

    return cmsModule;
  }

  private EventsModuleData updateEventsModuleData(EventsModuleData evenrModule, String name) {

    evenrModule.setTypeId("typeId");
    evenrModule.setId(102021L);
    evenrModule.setMarketsCount(10);
    evenrModule.setName(name);
    evenrModule.setNameOverride("eventModulesDta");
    evenrModule.setOutcomeId(BigInteger.valueOf(10));
    evenrModule.setOutcomeStatus(true);
    evenrModule.setEventSortCode("code");
    evenrModule.setStartTime(Instant.now().toString());
    evenrModule.setLiveServChannels("BYB");
    evenrModule.setLiveServChildrenChannels("banch");
    evenrModule.setLiveServLastMsgId("1213131");
    evenrModule.setCategoryId("10");
    evenrModule.setCategoryCode("CODE");
    evenrModule.setCategoryName("SPORTS");
    evenrModule.setClassId("044042010242");
    evenrModule.setClassName("SUFACEBETS");
    evenrModule.setTypeName("SPORTSTYPE");
    evenrModule.setCashoutAvail("true");
    evenrModule.setEventStatusCode("12121");
    evenrModule.setUS(true);
    evenrModule.setEventIsLive(true);
    evenrModule.setDisplayOrder(10);
    evenrModule.setStarted(true);
    evenrModule.setFinished(true);
    evenrModule.setOutright(true);
    evenrModule.setResponseCreationTime(Instant.now().toString());
    evenrModule.setLiveStreamAvailable(true);
    evenrModule.setDrilldownTagNames("21");
    evenrModule.setTypeFlagCodes("12");
    evenrModule.setTypeId("01xcl234322121");
    evenrModule.setBuildYourBetAvailable(true);
    evenrModule.setSsName("ssName");
    evenrModule.setMarkets(prepareOutputMarket());
    evenrModule.setPrimaryMarkets(prepareOutputMarket());
    RacingFormEvent revent = new RacingFormEvent();
    revent.setDistance("distance");
    revent.setGoing("going");
    evenrModule.setRacingFormEvent(revent);
    evenrModule.setGuid("2121212122");
    return evenrModule;
  }

  private List<OutputMarket> prepareOutputMarket() {
    OutputMarket market = new OutputMarket();
    List<OutputMarket> markets = new ArrayList<>();
    market.setId("qwwwwwq");
    market.setName("market");
    market.setLpAvailable(true);
    market.setSpAvailable(true);
    market.setGpAvailable(true);
    market.setEachWayAvailable(true);
    market.setEachWayFactorNum(11);
    market.setEachWayFactorDen(10);
    market.setEachWayFactorDen(10);
    market.setEachWayPlaces(10);
    market.setLiveServChannels("banch");
    market.setPriceTypeCodes("la");
    market.setNcastTypeCodes("la");
    market.setCashoutAvail("true");
    market.setHandicapType("la");
    market.setViewType("view");
    market.setMarketMeaningMajorCode("MC");
    market.setMarketMeaningMinorCode("MA");
    market.setTerms("terms");
    market.setMarketBetInRun(true);
    market.setRawHandicapValue(10.0);
    market.setDispSortName("name");
    market.setMarketStatusCode("CA");
    market.setTemplateMarketId(10L);
    market.setTemplateMarketName("marketname");
    market.setNextScore(10);
    market.setDrilldownTagNames("la");
    market.setDisplayOrder(3);
    markets.add(market);
    return markets;
  }

  public OutputPrice prepareOutputPrice() {
    OutputPrice oldPrice = new OutputPrice();
    oldPrice.setId("eeeqewqewqe");
    oldPrice.setPriceType("gdr");
    oldPrice.setPriceNum(12);
    oldPrice.setPriceDen(11);
    oldPrice.setPriceNum(10);
    oldPrice.setPriceDec(10.0);
    oldPrice.setHandicapValueDec("value");
    oldPrice.setRawHandicapValue(20.0);
    return oldPrice;
  }

  private void updateBasicRacingEventData(BasicRacingEventData basicRacingEventData, String name) {

    basicRacingEventData.setId("021201313123");
    basicRacingEventData.setName(name);
    basicRacingEventData.setStartTime(Instant.now().toString());
    basicRacingEventData.setGuid("b03131nndw123n1e21");
  }

  private Map<String, SegmentView> prepareModuleDataSegmentView(String moduleName) {
    Map<String, SegmentView> segmentMap = new HashMap<>();
    Map<String, SegmentOrderdModuleData> segmentModuleData = new HashMap<>();
    SegmentView view = new SegmentView();
    SegmentOrderdModuleData moduleData = new SegmentOrderdModuleData();
    moduleData.setSegmentOrder(1.0);
    if ("SurfaceBet".equals(moduleName)) {
      SurfaceBetModuleData surfaceBetModuleData = new SurfaceBetModuleData();
      // TODO:Need to add more fields
      surfaceBetModuleData.setTitle("surfaceBet");
      moduleData.setSurfaceBetModuleData(surfaceBetModuleData);
      segmentModuleData.put("s1", moduleData);
      view.setSurfaceBetModuleData(segmentModuleData);
    } else {

      QuickLinkData quickLinkData = new QuickLinkData();
      quickLinkData.setTitle("QuickLink");
      // TODO:Need to add more fields
      moduleData.setQuickLinkData(quickLinkData);
      segmentModuleData.put("s1", moduleData);
      view.setQuickLinkData(segmentModuleData);
    }

    segmentMap.put("s1", view);
    return segmentMap;
  }

  private void prepareInplayModuleDataSegmentView(InplayModule module) {
    Map<String, SegmentView> segmentMap = new HashMap<>();
    Map<String, SegmentOrderdModuleData> segmentModuleData = new HashMap<>();
    List<SegmentedEvents> limitedEvents = new ArrayList<>();
    SegmentedEvents segmentedEvent = new SegmentedEvents();
    segmentedEvent.setEventByTypeName(module.getData().get(0).getEventsByTypeName().get(0));
    segmentedEvent.setEvents(module.getData().get(0).getEventsByTypeName().get(0).getEvents());
    limitedEvents.add(segmentedEvent);
    SegmentView view = new SegmentView();
    SegmentOrderdModuleData moduleData = new SegmentOrderdModuleData();
    moduleData.setSegmentOrder(1.0);
    moduleData.setInplayData(module.getData().get(0));
    moduleData.setLimitedEvents(null);
    segmentModuleData.put("s1", moduleData);
    view.setInplayModuleData(segmentModuleData);

    segmentMap.put("s1", view);
    module.setModuleSegmentView(segmentMap);
  }

  private Map<String, SegmentView> prepareModuleSegmentView(String ModuleNmae) {
    Map<String, SegmentView> segmentMap = new HashMap<>();
    Map<String, SegmentOrderdModule> SegmentModuleData = new HashMap<>();
    SegmentView view = new SegmentView();
    SegmentOrderdModule moduleData = new SegmentOrderdModule();
    moduleData.setSegmentOrder(1.0);
    if ("HighlightCarousel".equals(ModuleNmae)) {
      HighlightCarouselModule highModuleData = new HighlightCarouselModule();
      // TODO:Need to add more fields
      highModuleData.setTitle("HighlightCarousel");
      moduleData.setHighlightCarouselModule(highModuleData);
      SegmentModuleData.put("s1", moduleData);
      view.setHighlightCarouselModules(SegmentModuleData);
    } else {
      EventsModule eventsModule = new EventsModule();
      // TODO:Need to add more fields
      eventsModule.setTitle("EventsModule");
      moduleData.setEventsModule(eventsModule);
      SegmentModuleData.put("s1", moduleData);
      view.setEventModules(SegmentModuleData);
    }
    segmentMap.put("s1", view);
    return segmentMap;
  }

  private void updateAbstractFeaturedModule(
      AbstractFeaturedModule featureModule, String id, String name) {
    if (id == null) {
      featureModule.setId("1213");
    } else {
      featureModule.setId(id);
    }
    featureModule.setPageType(FeaturedRawIndex.PageType.sport);
    featureModule.setSportId(16);
    featureModule.setTitle(name);
    featureModule.setDisplayOrder(BigDecimal.ZERO);
    featureModule.setSecondaryDisplayOrder(BigDecimal.ZERO);
    featureModule.setSortOrder(0.0);
    featureModule.setErrorMessage("error");
    featureModule.setSegmented(true);
    featureModule.setShowExpanded(true);
    featureModule.setPublishedDevices(Arrays.asList("desktop,tablet,mobile1".split(",")));
  }

  private void updateSegmentReferences(EventsModule module, String moduleTpe) {

    module.setSegments(Arrays.asList("s1".split(",")));
    List<SegmentReference> segmentReferences = new ArrayList<>();
    SegmentReference reference = new SegmentReference();
    reference.setSegment("s1");
    reference.setDisplayOrder(20.0);
    segmentReferences.add(reference);
    Map<String, SegmentView> moduleSegmentView = prepareModuleSegmentView(moduleTpe);
    module.setSegmentReferences(segmentReferences);
    module.setModuleSegmentView(moduleSegmentView);
  }

  private void updateEventModule(EventsModule module, ModuleType type) {
    module.setMaxRows(5);
    module.setMaxSelections(5);
    ModuleDataSelection dataSel = new ModuleDataSelection();
    dataSel.setSelectionId("435");
    dataSel.setSelectionType("type");
    module.setDataSelection(dataSel);
    Map<String, String> footerLink = new HashMap<>();
    footerLink.put("text", "");
    module.setFooterLink(footerLink);
    module.setCashoutAvail(true);
    module.setHasNoLiveEvents(true);
    List<String> outComeColumns = new ArrayList<>();
    outComeColumns.add("outcome");
    module.setOutcomeColumnsTitles(outComeColumns);
    module.setSpecial(true);
    module.setEnhanced(true);
    module.setYourCallAvailable(true);
    module.setTotalEvents(10);
    module.setCategoryId("121");
    module.setGroupedBySport(true);
    module.setModuleType(type);
  }
}
