package com.coral.oxygen.middleware.common.service

import com.coral.oxygen.middleware.common.service.featured.FeaturedModelChangeDetector
import com.coral.oxygen.middleware.common.utils.FanzoneConstants
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.RacingFormEvent
import com.coral.oxygen.middleware.pojos.model.output.featured.*
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.fasterxml.jackson.core.type.TypeReference
import com.fasterxml.jackson.databind.ObjectMapper
import spock.lang.Specification

import java.time.Instant

class FeaturedModelChangeDetectorSpec extends Specification {

  FeaturedModelChangeDetector structureChangeDetector
  FeaturedModel actual
  FeaturedModel previous
  public static final String SURFACE_SEGMENT = "SurfaceSegment"
  public static final String QUICKLINK_SEGMENT = "QuickLinkSegment";
  public static final String SEGMENT_TEST = "segmentTest"

  def setup() {
    structureChangeDetector = new FeaturedModelChangeDetector()

    def actualModelJson = getClass().getClassLoader().getResourceAsStream('featured_module_item.json')
    actual = new ObjectMapper().readValue(actualModelJson, new TypeReference<FeaturedModel>() { })

    def previousModelJson = getClass().getClassLoader().getResourceAsStream('featured_module_item.json')
    previous = new ObjectMapper().readValue(previousModelJson, new TypeReference<FeaturedModel>() { })
  }

  def "Previous Model is null"() {
    given:
    actual = new FeaturedModel()
    previous = null

    expect:
    structureChangeDetector.isChanged(actual, previous)
  }



  def "Size of models are not equal"() {
    given:
    previous.getModules().remove(0)

    expect:
    structureChangeDetector.isChanged(actual, previous)
  }

  def "Titles of models are not equal but structure is not changed"() {
    given:
    actual.setTitle('title')
    expect:
    !structureChangeDetector.isChanged(actual, previous)
  }

  def "Previous Inplay module is null"() {
    def module = new InplayModule()
    module.setId('1234')
    def previousModule = new InplayModule()
    module.setId('111')
    given:
    actual.modules.add(module)
    previous.modules.add(previousModule)
    expect:
    structureChangeDetector.isChanged(actual, previous)
  }
  def "Previous Model is null IsSChanged"() {
    given:
    actual = prepareModel("s1","s1")
    previous = prepareModel("s1","s1")

    expect:
    !structureChangeDetector.isChanged(actual, previous)
  }

  def "Previous Model id Equal  IsSChanged"() {
    given:
    actual = prepareModel("s1","s1")
    previous = prepareModel("s1","idChange")

    expect:
    structureChangeDetector.isChanged(actual, previous)
  }

  def "Previous order change  IsSChanged"() {
    given:
    actual = prepareModel("s1","orderChange1")
    previous = prepareModel("s1","orderChange2")

    expect:
    structureChangeDetector.isChanged(actual, previous)
  }


  def "Previous structure IsSChanged"() {
    given:
    actual = prepareModel("s1","StructureChanged1")
    previous = prepareModel("s1","StructureChanged2")
    expect:
    structureChangeDetector.isChanged(actual, previous)
  }

  def "PreviousModel is null IsSegmentWiseChanged"() {
    given:
    actual = prepareModel("s1","s1")
    previous = null

    expect:
    structureChangeDetector.isSegmentedModulesChanged(actual, previous)
  }

  def "PreviousModel is null IsFanzoneSegmentWiseChanged"() {
    given:
    actual = prepareModel("s1","s1")
    previous = null

    expect:
    structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }

  def "PreviousModel is not change IsSegmentWiseChanged"() {
    given:
    actual = prepareModel("s1","s1")
    previous = prepareModel("s1","s1")

    expect:
    !structureChangeDetector.isSegmentedModulesChanged(actual, previous)
  }

  def "PreviousModel is not change IsFanzoneSegmentWiseChanged"() {
    given:
    actual = prepareModel("s1","s1")
    previous = prepareModel("s1","s1")

    expect:
    !structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }


  def "PreviousModel is  change IsSegmentWiseChanged1"() {
    given:
    actual = prepareModel("s1","s1")
    previous = prepareModel("s1","s2")

    expect:
    structureChangeDetector.isSegmentedModulesChanged(actual, previous)
  }

  def "PreviousModel is  change IsSFanzoneegmentWiseChanged1"() {
    given:
    actual = prepareFanzoneModel("s1","s1")
    previous = prepareFanzoneModel("s1","s2")

    expect:
    structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }

  def "PreviousModel is  change IsSegmentWiseChanged"() {
    given:
    actual = prepareModel("s1","s1")
    previous = prepareModel("s2","s2")

    expect:
    structureChangeDetector.isSegmentedModulesChanged(actual, previous)
  }

  def "PreviousModel is  change IsFanzoneSegmentWiseChanged"() {
    given:
    actual = prepareFanzoneModel("s1","s1")
    previous = prepareFanzoneModel("s2","s2")

    expect:
    structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }



  def "PreviousModel is keyset empty  change IsFanzoneSegmentWiseChanged"() {
    given:
    actual = prepareFanzoneModelKeySetEmpty("s1","s1")
    previous = prepareFanzoneModelKeySetEmpty("s2","s2")

    expect:
    structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }

  def "PreviousModel is keyset empty  change IsSegmentWiseChanged"() {
    given:
    actual = prepareModelKeySetEmpty("s1","s1")
    previous = prepareModelKeySetEmpty("s2","s2")

    expect:
    structureChangeDetector.isSegmentedModulesChanged(actual, previous)
  }

  def "PreviousModel is  change isStructureChanged"() {
    given:
    actual = prepareModel("s1","s1")
    previous = prepareModel("s2","s2")

    expect:
    !structureChangeDetector.isStructureChanged(actual, previous)
  }

  def "PreviousModel is  change isFanzoneStructureChanged"() {
    given:
    actual = prepareFanzoneModel("s1","s1")
    previous = prepareFanzoneModel("s2","s2")

    expect:
    !structureChangeDetector.isStructureChanged(actual, previous)
  }


  def "actualModel segmentWise is null  change isStructureChanged"() {
    given:
    actual = prepareModel("s1","s1")
    previous = prepareModel("s2","s2")
    actual.segmentWiseModules=null;
    expect:
    !structureChangeDetector.isSegmentedModulesChanged(actual, previous)
  }

  def "actualModel fanzonesegmentWise is null  change isStructureChanged"() {
    given:
    actual = prepareFanzoneModel("s1","s1")
    previous = prepareFanzoneModel("s2","s2")
    actual.fanzoneSegmentWiseModules=null;
    expect:
    !structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }

  def "actualModel segmentWise HighLight keyset equal change isStructureChanged"() {
    given:
    actual = prepareModel("s1","s1")
    previous = prepareModel("s1","segmentTest")

    expect:
    structureChangeDetector.isSegmentedModulesChanged(actual, previous)
  }

  def "actualModel fanzonesegmentWise HighLight keyset equal change isStructureChanged"() {
    given:
    actual = prepareFanzoneModel("s1","s1")
    previous = prepareFanzoneModel("s1","segmentTest")

    expect:
    structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }

  def "actualModel segmentWise Quick link keyset equal change isStructureChanged"() {
    given:
    actual = prepareModel("s1","s1")
    previous = prepareModel("s1","QuickLinkSegment")

    expect:
    structureChangeDetector.isSegmentedModulesChanged(actual, previous)
  }
  def "actualModel fanzonesegmentWise Quick link keyset equal change isStructureChanged"() {
    given:
    actual = prepareFanzoneModel("s1","s1")
    previous = prepareFanzoneModel("s1","QuickLinkSegment")

    expect:
    structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }

  def "actualModel and previos model segmentWise Quick link keyset equal change isStructureChanged"() {
    given:
    actual = prepareModel("s1","QuickLinkSegment")
    previous = prepareModel("s1","QuickLinkSegment")

    expect:
    !structureChangeDetector.isSegmentedModulesChanged(actual, previous)
  }
  def "actualModel and previos model fanzonesegmentWise Quick link keyset equal change isStructureChanged"() {
    given:
    actual = prepareFanzoneModel("s1","QuickLinkSegment")
    previous = prepareFanzoneModel("s1","QuickLinkSegment")

    expect:
    !structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }

  def "actualModel segmentWise Quick link keyset is null equal change isStructureChanged"() {
    given:
    actual = prepareModel("s1","QuickLinkSegment")
    previous = prepareModel("s1","s1")

    expect:
    structureChangeDetector.isSegmentedModulesChanged(actual, previous)
  }
  def "actualModel fanzonesegmentWise Quick link keyset is null equal change isStructureChanged"() {
    given:
    actual = prepareFanzoneModel("s1","QuickLinkSegment")
    previous = prepareFanzoneModel("s1","s1")

    expect:
    structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }


  def "actualModel segmentWise SurfaceBet keyset equal change isStructureChanged"() {
    given:
    actual = prepareModel("s1","s1")
    previous = prepareModel("s1","SurfaceSegment")

    expect:
    structureChangeDetector.isSegmentedModulesChanged(actual, previous)
  }

  def "actualModel  fanzonesegmentWise SurfaceBet keyset equal change isStructureChanged"() {
    given:
    actual = prepareFanzoneModel("s1" , "s1")
    previous = prepareFanzoneModel("s1" , "SurfaceSegment")

    expect:
    structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }

  def "actualModel segmentWise SurfaceBet keyset null equal change isStructureChanged"() {
    given:
    actual = prepareModel("s1","SurfaceSegment")
    previous = prepareModel("s1","s1")

    expect:
    structureChangeDetector.isSegmentedModulesChanged(actual, previous)
  }

  def "actualModel fanzonesegmentWise SurfaceBet keyset null equal change isStructureChanged"() {
    given:
    actual = prepareFanzoneModel("s1","SurfaceSegment")
    previous = prepareFanzoneModel("s1","s1")

    expect:
    structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }

  def "actualModel and previous segmentWise SurfaceBet keyset null equal change isStructureChanged"() {
    given:
    actual = prepareModel("s1","SurfaceSegment")
    previous = prepareModel("s1","SurfaceSegment")

    expect:
    !structureChangeDetector.isSegmentedModulesChanged(actual, previous)
  }

  def "actualModel and previous fanzonesegmentWise SurfaceBet keyset null equal change isStructureChanged"() {
    given:
    actual = prepareFanzoneModel("s1","SurfaceSegment")
    previous = prepareFanzoneModel("s1","SurfaceSegment")

    expect:
    !structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }

  def "actualModel segmentWise null isStructureChanged"() {
    given:
    actual = prepareModel("s1","s1")
    previous = prepareModel("s1","SurfaceSegment")
    actual.setSegmentWiseModules(null);
    expect:
    !structureChangeDetector.isSegmentedModulesChanged(actual, previous)
  }
  def "actualModel segmentWise Inplay keyset equal change isStructureChanged"() {
    given:
    actual = prepareModel("s1","s1")
    previous = prepareModel("s1","s1")
    Map<String, SegmentView> segmentWiseModules = actual.getSegmentWiseModules()
    SegmentView segmentView = segmentWiseModules.get("s1")
    segmentView.setInplayModuleData(getSegmentInplayModule("s1"))
    actual.setSegmentWiseModules(segmentWiseModules)
    expect:
    structureChangeDetector.isSegmentedModulesChanged(actual, previous)
  }

  def "actualModel fanzonesegmentWise null isStructureChanged"() {
    given:
    actual = prepareFanzoneModel("s1","s1")
    previous = prepareFanzoneModel("s1","SurfaceSegment")
    actual.setFanzoneSegmentWiseModules(null);
    expect:
    !structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }


  def "PreviousModel is  change isOrderChanged"() {
    given:
    actual = prepareModel("s1","s1")
    previous = prepareModel("s2","s2")

    expect:
    !structureChangeDetector.isOrderChanged(actual, previous)
  }


  def "fanzonesegmentWise Bets Based On Your Team Module keyset equal change isStructureChanged"() {
    given:
    actual = prepareFZTeamBetsModel("s1", "s1")
    actual.fanzoneSegmentWiseModules["s1"].teamBetsModuleData = new HashMap<>()
    previous = prepareFZTeamBetsModel("s1", "s1")

    expect:
    structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }

  def "fanzonesegmentWise Bets Based On Other Fans Module keyset equal change isStructureChanged"() {
    given:
    actual = prepareFZFanBetsModel("s1", "s1")
    actual.fanzoneSegmentWiseModules["s1"].fanBetsModuleData = new HashMap<>()
    previous = prepareFZFanBetsModel("s1", "s1")

    expect:
    structureChangeDetector.isFanzoneSegmentedModulesChanged(actual, previous)
  }

  private static FeaturedModel prepareFZFanBetsModel(String viewSegment, String modulesSegment) {
    def view = new FanzoneSegmentView()
    def moduledata = new HashMap<String, FanBetsConfig>()

    def data = new FanBetsConfig(
        id: "fid",
        noOfMaxSelections: 4,
        pageType: FeaturedRawIndex.PageType.sport,
        guid: "875845"
        )

    moduledata[viewSegment] = data
    view.fanBetsModuleData = moduledata
    def featuredModel = new FeaturedModel(title: "ftitle")
    def fanzoneSegmentWiseModules = new HashMap<String, FanzoneSegmentView>()
    fanzoneSegmentWiseModules[modulesSegment] = view
    featuredModel.fanzoneSegmentWiseModules = fanzoneSegmentWiseModules

    def module = new FanBetsModule(
        title: "mtitle",
        pageType: FeaturedRawIndex.PageType.sport,
        id: "mid",
        data: [data]
        )

    featuredModel.modules = [module]

    return featuredModel
  }

  private static FeaturedModel prepareFZTeamBetsModel(String viewSegment, String modulesSegment) {
    def view = new FanzoneSegmentView()
    def moduledata = new HashMap<String, TeamBetsConfig>()

    def data = new TeamBetsConfig(
        id: "tid",
        noOfMaxSelections: 4,
        pageType: FeaturedRawIndex.PageType.sport,
        guid: "875845"
        )

    moduledata[viewSegment] = data
    view.teamBetsModuleData = moduledata
    def featuredModel = new FeaturedModel(title: "ftitle")
    def fanzoneSegmentWiseModules = new HashMap<String, FanzoneSegmentView>()
    fanzoneSegmentWiseModules[modulesSegment] = view
    featuredModel.fanzoneSegmentWiseModules = fanzoneSegmentWiseModules

    def module = new FanBetsModule(
        title: "mtitle",
        pageType: FeaturedRawIndex.PageType.sport,
        id: "mid",
        data: [data]
        )

    featuredModel.modules = [module]

    return featuredModel
  }

  private static FeaturedModel prepareModel(String segment,String s2) {
    EventsModuleData event = new EventsModuleData()
    event.setName("event")
    event.setId(1L)

    EventsModule sampleModule = new EventsModule()
    sampleModule.setId("_id")
    if("idChange".equals(s2))
      sampleModule.setId("_id1")
    sampleModule.setCashoutAvail(true)
    sampleModule.setData(Arrays.asList(event))

    FeaturedModel page = new FeaturedModel()
    if("orderChange1".equals(s2)){
      List<EventsModule> datas=new ArrayList<>();

      EventsModule sampleModule1 = new EventsModule()
      sampleModule1.setId("id2");
      sampleModule1.setTitle("title");
      datas.add(sampleModule1);
      datas.add(sampleModule);
      page.setModules(datas)
    }else if("orderChange2".equals(s2)){
      List<EventsModule> datas=new ArrayList<>();
      datas.add(sampleModule);
      EventsModule sampleModule1 = new EventsModule()
      sampleModule1.setId("id2");
      sampleModule1.setTitle("title");
      datas.add(sampleModule1);
      page.setModules(datas)
    }else if("StructureChanged1".equals(s2)) {
      List<EventsModule> datas=new ArrayList<>();
      datas.add(sampleModule);
      EventsModule sampleModule1 = new EventsModule()
      sampleModule1.setId("id24");
      sampleModule1.setTitle("title1");
      datas.add(sampleModule1);
      page.setModules(datas)
    }else if("StructureChanged2".equals(s2)) {
      List<EventsModule> datas=new ArrayList<>();
      datas.add(sampleModule);
      EventsModule sampleModule1 = new EventsModule()
      sampleModule1.setId("id24");
      sampleModule1.setTitle("title4");
      datas.add(sampleModule1);
      page.setModules(datas)
    }else {
      page.setModules(Arrays.asList(sampleModule))
    }
    page.setPageId("0")
    Map<Long, FeaturedModel> storageResult = new HashMap<>()
    storageResult.put(1L, page)
    Map<String, SegmentView> segmentWiseModules = new HashMap<>()
    segmentWiseModules.put(segment,prepareSegmentView(s2))
    page.setSegmentWiseModules(segmentWiseModules)
    return page
  }

  private static FeaturedModel prepareFanzoneModel(String segment,String s2) {
    EventsModuleData event = new EventsModuleData()
    event.setName("event")
    event.setId(1L)

    EventsModule sampleModule = new EventsModule()
    sampleModule.setId("_id")
    if("idChange".equals(s2))
      sampleModule.setId("_id1")
    sampleModule.setCashoutAvail(true)
    sampleModule.setData(Arrays.asList(event))

    FeaturedModel page = new FeaturedModel()
    if("orderChange1".equals(s2)){
      List<EventsModule> datas=new ArrayList<>();

      EventsModule sampleModule1 = new EventsModule()
      sampleModule1.setId("id2");
      sampleModule1.setTitle("title");
      datas.add(sampleModule1);
      datas.add(sampleModule);
      page.setModules(datas)
    }else if("orderChange2".equals(s2)){
      List<EventsModule> datas=new ArrayList<>();
      datas.add(sampleModule);
      EventsModule sampleModule1 = new EventsModule()
      sampleModule1.setId("id2");
      sampleModule1.setTitle("title");
      datas.add(sampleModule1);
      page.setModules(datas)
    }else if("StructureChanged1".equals(s2)) {
      List<EventsModule> datas=new ArrayList<>();
      datas.add(sampleModule);
      EventsModule sampleModule1 = new EventsModule()
      sampleModule1.setId("id24");
      sampleModule1.setTitle("title1");
      datas.add(sampleModule1);
      page.setModules(datas)
    }else if("StructureChanged2".equals(s2)) {
      List<EventsModule> datas=new ArrayList<>();
      datas.add(sampleModule);
      EventsModule sampleModule1 = new EventsModule()
      sampleModule1.setId("id24");
      sampleModule1.setTitle("title4");
      datas.add(sampleModule1);
      page.setModules(datas)
    }else {
      page.setModules(Arrays.asList(sampleModule))
    }
    page.setPageId(FanzoneConstants.FANZONE_PAGE_ID)
    Map<Long, FeaturedModel> storageResult = new HashMap<>()
    storageResult.put(1L, page)
    Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules = new HashMap<>()
    fanzoneSegmentWiseModules.put(segment,prepareFanzoneSegmentView(s2))
    page.setFanzoneSegmentWiseModules(fanzoneSegmentWiseModules)
    return page
  }

  private static FeaturedModel prepareModelKeySetEmpty(String segment,String s2) {
    EventsModuleData event = new EventsModuleData()
    event.setName("event")
    event.setId(1L)

    EventsModule sampleModule = new EventsModule()
    sampleModule.setId("_id")
    sampleModule.setCashoutAvail(true)
    sampleModule.setData(Arrays.asList(event))

    FeaturedModel page = new FeaturedModel()
    page.setModules(Arrays.asList(sampleModule))
    page.setPageId("0")
    Map<Long, FeaturedModel> storageResult = new HashMap<>()
    storageResult.put(1L, page)
    Map<String, SegmentView> segmentWiseModules = new HashMap<>()
    segmentWiseModules.put(segment,prepareSegmentView(s2))
    page.setSegmentWiseModules(segmentWiseModules)
    return page
  }

  private static FeaturedModel prepareFanzoneModelKeySetEmpty(String segment,String s2) {
    EventsModuleData event = new EventsModuleData()
    event.setName("event")
    event.setId(1L)

    EventsModule sampleModule = new EventsModule()
    sampleModule.setId("_id")
    sampleModule.setCashoutAvail(true)
    sampleModule.setData(Arrays.asList(event))

    FeaturedModel page = new FeaturedModel()
    page.setModules(Arrays.asList(sampleModule))
    page.setPageId(FanzoneConstants.FANZONE_PAGE_ID)
    Map<Long, FeaturedModel> storageResult = new HashMap<>()
    storageResult.put(1L, page)
    Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules = new HashMap<>()
    fanzoneSegmentWiseModules.put(segment,prepareFanzoneSegmentView(s2))
    page.setFanzoneSegmentWiseModules(fanzoneSegmentWiseModules)
    return page
  }


  private static SegmentView prepareSegmentView(String s) {

    SegmentView view=new SegmentView();
    view.setEventModules(getSegmentEventModuleMap(s))
    view.setHighlightCarouselModules(getSegmentHighLightModuleMap(s))
    if(!"SurfaceSegment".equals(s))
      view.setSurfaceBetModuleData(getSegmentSurfaceModule(s))
    if(!"QuickLinkSegment".equals(s))
      view.setQuickLinkData(getSegmentQuickLinkModule(s))
    return view
  }

  private static FanzoneSegmentView prepareFanzoneSegmentView(String s) {

    FanzoneSegmentView view=new FanzoneSegmentView();
    view.setHighlightCarouselModules(getFanzoneSegmentHighLightModuleMap(s))
    if(!SURFACE_SEGMENT.equals(s))
      view.setSurfaceBetModuleData(getFanzoneSegmentSurfaceModule(s))
    if(!QUICKLINK_SEGMENT.equals(s))
      view.setQuickLinkModuleData(getFanzoneQuickLinkModule(s))
    return view
  }

  private static  Map<String, SegmentOrderdModuleData> getSegmentSurfaceModule(String segment){

    Map<String, SegmentOrderdModuleData> eventModule=new HashMap<>();
    SegmentOrderdModuleData orderModule=new SegmentOrderdModuleData();
    orderModule.setSegmentOrder(10);
    orderModule.setSurfaceBetModuleData(createSurfaceModuledata())
    eventModule.put(segment,orderModule)
    return eventModule;
  }

  private static  Map<String, SurfaceBetModuleData> getFanzoneSegmentSurfaceModule(String segment){
    Map<String, SurfaceBetModuleData> eventModule=new HashMap<>();
    eventModule.put(segment,createSurfaceModuledata())
    return eventModule;
  }

  private static  Map<String, SegmentOrderdModuleData> getSegmentQuickLinkModule(String segment){

    Map<String, SegmentOrderdModuleData> eventModule=new HashMap<>();
    SegmentOrderdModuleData orderModule=new SegmentOrderdModuleData();
    orderModule.setSegmentOrder(10);
    orderModule.setQuickLinkData(createQuickLinkData())
    eventModule.put(segment,orderModule)
    return eventModule;
  }
  private static  Map<String, QuickLinkData> getFanzoneQuickLinkModule(String segment){
    Map<String, QuickLinkData> eventModule=new HashMap<>();
    eventModule.put(segment,createQuickLinkData())
    return eventModule;
  }

  private static  Map<String, SegmentOrderdModule> getSegmentEventModuleMap(String segment){

    Map<String, SegmentOrderdModule> eventModule=new HashMap<>();
    SegmentOrderdModule orderModule=new SegmentOrderdModule();
    orderModule.setSegmentOrder(10);

    orderModule.setEventsModule(getEventModuleData());
    if("segmentTest".equals(segment)||"QuickLinkSegment".equals(segment)||"SurfaceSegment".equals(segment)) {
      eventModule.put("s1", orderModule)
    }else{
      eventModule.put(segment, orderModule)
    }
    return eventModule;
  }

  private static  Map<String, SegmentOrderdModule> getSegmentHighLightModuleMap(String segment){

    Map<String, SegmentOrderdModule> highlightModule=new HashMap<>();
    SegmentOrderdModule orderModule=new SegmentOrderdModule();
    orderModule.setSegmentOrder(10);

    orderModule.setHighlightCarouselModule(getHighlightCarouselModuleData());
    if("segmentTest".equals(segment)){
      highlightModule.put(segment,orderModule)
      highlightModule.put("s1",orderModule)
    }else if("QuickLinkSegment".equals(segment)){
      highlightModule.put("s1",orderModule)
    }else if("SurfaceSegment".equals(segment)){
      highlightModule.put("s1",orderModule)
    }else{
      highlightModule.put(segment, orderModule)
    }
    return highlightModule;
  }

  private static  Map<String, HighlightCarouselModule> getFanzoneSegmentHighLightModuleMap(String segment){

    Map<String, HighlightCarouselModule> highlightModule =new HashMap<>();

    if(SEGMENT_TEST.equals(segment)){
      highlightModule.put(segment,getHighlightCarouselModuleData())
      highlightModule.put("s1",getHighlightCarouselModuleData())
    }else if(SURFACE_SEGMENT.equals(segment)){
      highlightModule.put("s1",getHighlightCarouselModuleData())
    }else if(QUICKLINK_SEGMENT.equals(segment)){
      highlightModule.put("s1",getHighlightCarouselModuleData())
    } else{
      highlightModule.put(segment, getHighlightCarouselModuleData())
    }
    return highlightModule;
  }

  private static  Map<String, SegmentOrderdModuleData> getSegmentInplayModule(String segment){

    Map<String, SegmentOrderdModuleData> inplayModule=new HashMap<>();
    SegmentOrderdModuleData orderModule=new SegmentOrderdModuleData();
    orderModule.setSegmentOrder(10);
    orderModule.setInplayData(createInplayData())
    inplayModule.put(segment,orderModule)
    return inplayModule;
  }

  private static EventsModule getEventModuleData(){
    EventsModuleData event = new EventsModuleData()
    event.setName("event")
    event.setId(1L)

    EventsModule sampleModule = new EventsModule()
    sampleModule.setId("_id")
    sampleModule.setCashoutAvail(true)
    sampleModule.setData(Arrays.asList(event))
    return sampleModule;
  }


  private static HighlightCarouselModule getHighlightCarouselModuleData(){
    EventsModuleData event = new EventsModuleData()
    event.setName("event")
    event.setId(1L)

    HighlightCarouselModule sampleModule = new HighlightCarouselModule()
    sampleModule.setId("_id")
    sampleModule.setCashoutAvail(true)
    sampleModule.setData(Arrays.asList(event))
    return sampleModule;
  }

  public static QuickLinkData createQuickLinkData(){


    QuickLinkData moduledata = new QuickLinkData();

    moduledata.setId("abd031def0313d10212");
    moduledata.setDestination("setDestination");
    moduledata.setSvgId("svgid");
    moduledata.setDisplayOrder(10);
    moduledata.setTitle("title");
    moduledata.setGuid("guid");
    return moduledata;
  }

  public static  SurfaceBetModuleData createSurfaceModuledata() {

    SurfaceBetModuleData moduledate = new SurfaceBetModuleData();
    moduledate.setTitle("SurfaceBetModule");
    moduledate.setContent("surfaceContent");
    moduledate.setSvgId("id");
    moduledate.setSelectionId(10);
    moduledate.setObjId("q09olki87jh7171771");
    moduledate.setTypeId("type");
    moduledate.setSvgBgId("Image1");
    moduledate.setSvgBgImgPath("image1");
    moduledate.setContentHeader("Content Header");
    updateEventsModuleData(moduledate, "surfacebetmoduledata");
    return moduledate;
  }

  private static EventsModuleData updateEventsModuleData(EventsModuleData evenrModule, String name) {

    evenrModule.setTypeId("typeId");
    evenrModule.setId(102021L);
    evenrModule.setMarketsCount(10);
    evenrModule.setName(name);
    evenrModule.setNameOverride("eventModulesDta");
    evenrModule.setOutcomeId(10L);
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
    RacingFormEvent revent = new RacingFormEvent();
    revent.setDistance("distance");
    revent.setGoing("going");
    evenrModule.setRacingFormEvent(revent);
    evenrModule.setGuid("2121212122");
    return evenrModule;
  }

  public static SportSegment createInplayData(){


    SportSegment sportSegment = new SportSegment();

    sportSegment.setSvgId("svgid");
    sportSegment.setDisplayOrder(10);
    sportSegment.setGuid("guid");
    return sportSegment;
  }
}
