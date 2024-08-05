package com.coral.oxygen.middleware.featured.consumer.sportpage
import com.coral.oxygen.middleware.common.mappers.ExternalKeyMapper
import com.coral.oxygen.middleware.common.mappers.SiteServeChildrenMapper
import com.coral.oxygen.middleware.common.mappers.RacingModuleDataMapper
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService
import com.coral.oxygen.middleware.featured.consumer.sportpage.racing.InternationalToteRacingModuleService
import com.coral.oxygen.middleware.featured.consumer.sportpage.racing.RacingEventModuleService
import com.coral.oxygen.middleware.featured.consumer.sportpage.racing.VirtualCarouselRacingModuleService
import com.coral.oxygen.middleware.featured.service.injector.ConsumeBirHREvents
import com.coral.oxygen.middleware.featured.service.injector.FeaturedSiteServerService
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig
import com.coral.oxygen.middleware.pojos.model.cms.featured.CmsRacingModule
import com.coral.oxygen.middleware.pojos.model.cms.featured.RacingConfig
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule
import com.coral.oxygen.middleware.pojos.model.output.InternationalToteRaceData
import com.coral.oxygen.middleware.pojos.model.output.RacingEventData
import com.coral.oxygen.middleware.pojos.model.output.ReferenceEachWayTerms
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.api.SiteServerImpl
import com.egalacoral.spark.siteserver.model.Category
import com.egalacoral.spark.siteserver.model.Children
import com.egalacoral.spark.siteserver.model.Event
import com.egalacoral.spark.siteserver.model.ExternalKeys
import com.egalacoral.spark.siteserver.model.Market
import com.egalacoral.spark.siteserver.model.Outcome
import com.egalacoral.spark.siteserver.model.Pool
import com.egalacoral.spark.siteserver.model.ReferenceEachWayTerms
import org.apache.commons.lang3.StringUtils
import spock.lang.Shared
import spock.lang.Specification
import java.time.Duration
import java.util.function.BiConsumer

import static com.coral.oxygen.middleware.featured.utils.FeaturedDataUtils.getSSEventsFromResource

class RacingModuleProcessorSpec extends Specification {
  private static final int HORSE_RACING_CATEGORY_ID = 21
  RacingModuleProcessor racingModuleProcessor
  FeaturedSiteServerService siteServerService
  //ConsumeBirHREvents consumeBirHREvents
  ConsumeBirHREvents consumeBirHREventsMock
  CmsSystemConfig systemConfig
  @Shared
  List<Children> events
  void setup() {
    events = getSSEventsFromResource("injector_horse_racing_ids.json")
    siteServerService = Mock(FeaturedSiteServerService)
    def racingDataMapper = new RacingModuleDataMapper()
    def externalKeyMapper = new ExternalKeyMapper()
    def siteServeChildrenMapper = new SiteServeChildrenMapper()
    def siteServerApi = new SiteServerImpl(new SiteServerApi.Builder())
    def marketTemplateNameService = new MarketTemplateNameService()
    //def consumeBirHREvents = new ConsumeBirHREvents(siteServerApi,marketTemplateNameService)
    consumeBirHREventsMock = Mock(ConsumeBirHREvents)
    def eventModuleService = new RacingEventModuleService(siteServerService, racingDataMapper, externalKeyMapper, siteServeChildrenMapper,consumeBirHREventsMock)
    def virtualCarouselService = new VirtualCarouselRacingModuleService(siteServerService, racingDataMapper)
    def intToteService = new InternationalToteRacingModuleService(siteServerService, racingDataMapper, externalKeyMapper, siteServeChildrenMapper)
    racingModuleProcessor = new RacingModuleProcessor(eventModuleService, virtualCarouselService,  intToteService)
    systemConfig = Mock(CmsSystemConfig)
  }
  def "ProcessModule unsupported"() {
    when:
    racingModuleProcessor.processModule(createRacingSportPageModule(HORSE_RACING_CATEGORY_ID, Collections.emptyList()), systemConfig, Collections.emptySet())
    then:
    thrown(UnsupportedOperationException)
  }
  def "ProcessModules with totePoolIndicators enabled"() {
    given:
    def categoryId = String.valueOf(HORSE_RACING_CATEGORY_ID)
    def sportModule = createRacingSportPageModule(HORSE_RACING_CATEGORY_ID, [
      createRacingConfig(HORSE_RACING_CATEGORY_ID, "UIR", true, 285)
    ])
    siteServerService.getActiveClassesWithOpenEvents(categoryId) >> [createClass(223, categoryId)]
    def expectedEventId = "12345"
    when:
    def featuredModules = racingModuleProcessor.processModules(sportModule, systemConfig, Collections.emptySet())
    then:
    1 * siteServerService.getVirtualRacingEventsAndExternalKeys(*_) >> [
      children(createEvent(expectedEventId, "234", "12", "GVA,UK,NE,PVA,QL,RVA,VR"), { child, event -> child.setEvent(event) }),
      children(createExternalKey("OBEvLinkTote", "event", "1234" + "," + "54332" + ",event"), { child, keys -> child.setExternalKeys(keys) })
    ]
    1 * siteServerService.getPoolTypes(*_) >> Collections.emptyList()
    featuredModules.size() == 1
    featuredModules[0].getId() == sportModule.getSportModule().getId()
    featuredModules[0].getSportId() == sportModule.getSportModule().getSportId()
    featuredModules[0].getTitle() == sportModule.getSportModule().getTitle()
    featuredModules[0].getData().size() == 1
    featuredModules[0].getData()[0] instanceof RacingEventData
    def racingEvent = featuredModules[0].getData()[0] as RacingEventData
    racingEvent.getId() == expectedEventId
  }
  def "ProcessModules with totePoolIndicators"() {
    given:
    def categoryId = String.valueOf(HORSE_RACING_CATEGORY_ID)
    def sportModule = createRacingSportPageModule(HORSE_RACING_CATEGORY_ID, [
      createRacingConfig(HORSE_RACING_CATEGORY_ID, "UIR", true, 285)
    ])
    def expectedEvent = createEvent("12345", "231", "75", "UK,NE,PVA,QL,RVA,VR")
    def externalEvent = createEvent("54332", "23", "751", "")
    def expectedPool = createPool("23,156478386,156478387,156478388")
    siteServerService.getActiveClassesWithOpenEvents(categoryId) >> [createClass(223, categoryId)]
    when:
    def featuredModules = racingModuleProcessor.processModules(sportModule, systemConfig, Collections.emptySet())
    then:
    1 * siteServerService.getVirtualRacingEventsAndExternalKeys(*_) >> [
      children(expectedEvent, { child, event -> child.setEvent(event) }),
      children(createExternalKey("OBEvLinkTote", "event", "12345" + "," + "54332" + ",event"), { child, keys -> child.setExternalKeys(keys) })
    ]
    1 * siteServerService.getPoolTypes(*_) >> [expectedPool]
    1 * siteServerService.getAllEventToMarketForEvent(*_) >> [externalEvent]
    featuredModules.size() == 1
    featuredModules[0].getId() == sportModule.getSportModule().getId()
    featuredModules[0].getSportId() == sportModule.getSportModule().getSportId()
    featuredModules[0].getTitle() == sportModule.getSportModule().getTitle()
    featuredModules[0].getData().size() == 1
    featuredModules[0].getData()[0] instanceof RacingEventData
    def event = featuredModules[0].getData()[0] as RacingEventData
    event.getId() == expectedEvent.getId()
    event.getPoolTypes().size() == 1
    event.getPoolTypes()[0] == expectedPool.getType()
  }
  def "ProcessModules with totePoolIndicators disabled"() {
    given:
    def categoryId = String.valueOf(HORSE_RACING_CATEGORY_ID)
    def sportModule = createRacingSportPageModule(HORSE_RACING_CATEGORY_ID, [
      createRacingConfig(HORSE_RACING_CATEGORY_ID, "UIR", false, 285)
    ])
    this.consumeBirHREventsMock.consumeBirEvents() >> events
    siteServerService.getActiveClassesWithOpenEvents(categoryId) >> [createClass(223, categoryId)]
    when:
    def featuredModules = racingModuleProcessor.processModules(sportModule, systemConfig, Collections.emptySet())
    then:
    1 * siteServerService.getVirtualRacingEvents(*_) >> [
      createEvent("12345", "456", "98", "UK")
    ]
    0 * siteServerService.getPoolTypes(*_)
    featuredModules.size() == 1
  }
  def "ProcessModules with no outcomes"() {
    given:
    def categoryId = String.valueOf(HORSE_RACING_CATEGORY_ID)
    def sportModule = createRacingSportPageModule(HORSE_RACING_CATEGORY_ID, [
      createRacingConfig(HORSE_RACING_CATEGORY_ID, "UIR", false, 285)
    ])
    siteServerService.getActiveClassesWithOpenEvents(categoryId) >> [createClass(223, categoryId)]
    when:
    def featuredModules = racingModuleProcessor.processModules(sportModule, systemConfig, Collections.emptySet())
    then:
    1 * siteServerService.getVirtualRacingEvents(*_) >> [
      createEvent("12345", "456", null, null)
    ]
    0 * siteServerService.getPoolTypes(*_)
    featuredModules.size() == 0
    //featuredModules.get(0).getData().isEmpty()
  }
  def "ProcessModules with VIRTUAL_RACE_CAROUSEL type"() {
    given:
    def sportModule = createRacingSportPageModule(HORSE_RACING_CATEGORY_ID, [
      createRacingConfig(HORSE_RACING_CATEGORY_ID, "VRC", true, 285)
    ])
    when:
    def featuredModules = racingModuleProcessor.processModules(sportModule, systemConfig, Collections.emptySet())
    then:
    1 * siteServerService.getNextRaces("285", "1,3,4") >> Collections.emptyList()
    featuredModules.size() == 1
  }
  def "ProcessModules with INTERNATIONAL_TOTE_RACING type"() {
    given:
    def sportModule = createRacingSportPageModule(HORSE_RACING_CATEGORY_ID, [
      createRacingConfig(HORSE_RACING_CATEGORY_ID, "ITC", false, 16288)
    ])
    def expectedEventId = "1234567"
    when:
    def featuredModules = racingModuleProcessor.processModules(sportModule, systemConfig, Collections.emptySet())
    then:
    1 * siteServerService.getInternationalToteRacingEventsAndExternalKeys(["16288"], Duration.ofHours(24)) >>
    [
      children(createEvent(expectedEventId, null, null, null), { child, event -> child.setEvent(event) }),
      children(createExternalKey("OBEvLinkNonTote", "event", expectedEventId + ",54332,event,2,22,event,"), { child, keys -> child.setExternalKeys(keys) })
    ]
    featuredModules.size() == 1
    def actualModule = featuredModules.get(0)
    actualModule.getSportId() == HORSE_RACING_CATEGORY_ID
    actualModule.getData().size() == 1
    def data = actualModule.getData().get(0) as InternationalToteRaceData
    data.getId() == expectedEventId
    data.getExternalKeys().size() == 1
    data.getExternalKeys().containsKey("OBEvLinkNonTote")
    data.getExternalKeys().get("OBEvLinkNonTote") == "54332"
  }
  def "Sort modules with INTERNATIONAL_TOTE_RACING type"() {
    given:
    def sportModule = createRacingSportPageModule(HORSE_RACING_CATEGORY_ID, [
      createRacingConfig(HORSE_RACING_CATEGORY_ID, "ITC", false, 16288)
    ])
    def notResulted = createEvent("1", null, null, null)
    notResulted.isResulted() >> Boolean.FALSE
    def resulted = createEvent("2", null, null, null)
    resulted.isResulted() >> Boolean.TRUE
    siteServerService.getInternationalToteRacingEventsAndExternalKeys(["16288"], Duration.ofHours(24)) >>
    [
      children(notResulted, { child, event -> child.setEvent(event) }),
      children(resulted, { child, event -> child.setEvent(event) }),
      children(createExternalKey("OBEvLinkNonTote", "event", "1,54332,event,2,43,event"), { child, keys -> child.setExternalKeys(keys) })
    ]
    when:
    def featuredModules = racingModuleProcessor.processModules(sportModule, systemConfig, Collections.emptySet())
    then:
    def actualModule = featuredModules.get(0)
    actualModule.getData().size() == 2
    def data = actualModule.getData().get(0) as InternationalToteRaceData
    data.getId() == "1"
  }
  def "Sort modules by startTime with INTERNATIONAL_TOTE_RACING type"() {
    given:
    def sportModule = createRacingSportPageModule(HORSE_RACING_CATEGORY_ID, [
      createRacingConfig(HORSE_RACING_CATEGORY_ID, "ITC", false, 16288)
    ])
    def notResulted = createEvent("1", null, null, null)
    def resulted = createEvent("2", null, null, null)
    resulted.isResulted() >> Boolean.TRUE
    def resultedWithStartTime = createEvent("3", null, null, null)
    resultedWithStartTime.isResulted() >> Boolean.TRUE
    resultedWithStartTime.getStartTime() >> "2020-09-11T03:21:21Z"
    siteServerService.getInternationalToteRacingEventsAndExternalKeys(["16288"], Duration.ofHours(24)) >>
    [
      children(notResulted, { child, event -> child.setEvent(event) }),
      children(resulted, { child, event -> child.setEvent(event) }),
      children(resultedWithStartTime, { child, event -> child.setEvent(event) }),
      children(createExternalKey("OBEvLinkNonTote", "event", "1,54332,event,2,43,event,3,32,event"), { child, keys -> child.setExternalKeys(keys) })
    ]
    when:
    def featuredModules = racingModuleProcessor.processModules(sportModule, systemConfig, Collections.emptySet())
    then:
    def actualModule = featuredModules.get(0)
    actualModule.getData().size() == 3
    def data = actualModule.getData().get(0) as InternationalToteRaceData
    data.getId() == "3"
  }
  def "ProcessModules with scoop6"() {
    given:
    def categoryId = String.valueOf(HORSE_RACING_CATEGORY_ID)
    def sportModule = createRacingSportPageModule(HORSE_RACING_CATEGORY_ID, [
      createRacingConfig(HORSE_RACING_CATEGORY_ID, "UIR", true, 285)
    ])
    siteServerService.getActiveClassesWithOpenEvents(categoryId) >> [createClass(223, categoryId)]
    when:
    def featuredModules = racingModuleProcessor.processModules(sportModule, systemConfig, Collections.emptySet())
    then:
    1 * siteServerService.getVirtualRacingEventsAndExternalKeys(*_) >> [
      children(createEvent("e1", "234", "12", "GVA,UK,NE,PVA,QL,RVA,VR"), { child, event -> child.setEvent(event) }),
      children(createEvent("e2", "235", "13", "GVA,UK,NE,PVA,QL,RVA,VR"), { child, event -> child.setEvent(event) }),
      children(createExternalKey("OBEvLinkTote", "event", "e1" + "," + "eE1" + ",event"+",e2"+",eE3"+",event"), { child, keys -> child.setExternalKeys(keys) }),
      children(createExternalKey("OBEvLinkScoop6", "event", "e1" + "," + "eE2" + ",event"), { child, keys -> child.setExternalKeys(keys) })
    ]
    1 * siteServerService.getPoolTypes(*_) >> getPools()
    1 * siteServerService.getAllEventToMarketForEvent(*_) >> getExternalEventMarkets()
    featuredModules.size() == 1
    def racingEvent = featuredModules[0].getData()[0] as RacingEventData
    racingEvent.getPoolTypes() == ["USC6", "UQDP"]
    racingEvent.getId() == "e1"
    def racingEvent1 = featuredModules[0].getData()[1] as RacingEventData
    racingEvent1.getPoolTypes() == ["UPLP"]
    racingEvent1.getId() == "e2"
  }
  private Category createClass(Integer id, String categoryId) {
    def eventClass = Mock(Category)
    eventClass.getCategoryId() >> categoryId
    eventClass.getId() >> id
    eventClass
  }
  private static SportPageModule createRacingSportPageModule(int categoryId, List<CmsRacingModule> moduleItems) {
    def racingSportModule = new SportModule.SportModuleBuilder()
        .id("1")
        .brand("bma")
        .title("Racing module")
        .moduleType(ModuleType.RACING_MODULE)
        .pageType(FeaturedRawIndex.PageType.sport)
        .sportId(categoryId)
        .publishedDevices(Collections.emptyList())
        .build()
    new SportPageModule(racingSportModule, moduleItems)
  }
  CmsRacingModule createRacingConfig(int categoryId, String racingModuleAbbreviation, boolean enabledPoolIndicators, Integer classId) {
    def config = new RacingConfig()
    config.setAbbreviation(racingModuleAbbreviation)
    config.setEnablePoolIndicators(enabledPoolIndicators)
    config.setClassId(classId)
    config.setExcludeTypeIds("1,3,4")
    def racingModule = new CmsRacingModule()
    racingModule.setId("1")
    racingModule.setPageType(FeaturedRawIndex.PageType.sport)
    racingModule.setSportId(categoryId)
    racingModule.setType(ModuleType.RACING_MODULE.name())
    racingModule.setRacingConfig(config)
    racingModule.setActive(true)
    racingModule
  }
  private Event createEvent(String id, String marketId, String outcomeId, String flagCodes) {
    def event = Mock(Event)
    event.getId() >> id
    event.getTypeFlagCodes() >> flagCodes
    if (StringUtils.isNotBlank(marketId)) {
      def market = Mock(Market)
      market.getId() >> marketId
      market.getEventId() >> id
      event.getMarkets() >> [market]
      if (StringUtils.isNotBlank(outcomeId)) {
        def outcome = Mock(Outcome)
        outcome.getId() >> outcomeId
        outcome.getMarketId() >> marketId
        outcome.getPrices() >> []
        market.getOutcomes() >> [outcome]
      }
      def referenceEachWayTerms = Mock(ReferenceEachWayTerms)
      referenceEachWayTerms.getId() >> "1"
      referenceEachWayTerms.getPlaces() >> 1
      market.getReferenceEachWayTerms() >> [referenceEachWayTerms]
    }
    event
  }
  private static ExternalKeys createExternalKey(String type, String recordType, String mapping) {
    def externalKeys = new ExternalKeys()
    externalKeys.setExternalKeyTypeCode(type)
    externalKeys.setRefRecordType(recordType)
    externalKeys.setMappings(mapping)
    externalKeys
  }
  static Pool createPool(String marketIds) {
    Pool pool = new Pool()
    pool.setId("12")
    pool.setType("UQDP")
    pool.setMarketIds(marketIds)
    pool
  }
  static <T> Children children(T childEntity, BiConsumer<Children, T> setChildrenEntity) {
    def child = new Children()
    setChildrenEntity.accept(child, childEntity)
    child
  }
  static List<Pool> getPools(){
    List<Pool> pools = new ArrayList<>();
    Pool pool = new Pool()
    pool.setId("12")
    pool.setType("UQDP")
    pool.setMarketIds("M1,M2")
    pools.add(pool)
    Pool pool1 = new Pool()
    pool1.setId("13")
    pool1.setType("USC6")
    pool1.setMarketIds("M2")
    pools.add(pool1)
    Pool pool2 = new Pool()
    pool2.setId("14")
    pool2.setType("UPLP")
    pool2.setMarketIds("M3")
    pools.add(pool2)
    pools
  }
  List<Event> getExternalEventMarkets(){
    List<Event> eventList = new ArrayList<>();
    eventList.add(createEvent("eE1", "M1", "12", "GVA,UK,NE,PVA,QL,RVA,VR"))
    eventList.add(createEvent("eE2", "M2", "13", "GVA,UK,NE,PVA,QL,RVA,VR"))
    eventList.add(createEvent("eE3", "M3", "14", "GVA,UK,NE,PVA,QL,RVA,VR"))
    eventList
  }
}
