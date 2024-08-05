package com.oxygen.publisher.inplay.service

import com.corundumstudio.socketio.BroadcastOperations
import com.corundumstudio.socketio.SocketIOServer
import com.fasterxml.jackson.databind.ObjectMapper
import com.oxygen.publisher.configuration.JsonSupportConfig
import com.oxygen.publisher.inplay.InplayServiceRegistry
import com.oxygen.publisher.inplay.configuration.InplayServiceConfiguration
import com.oxygen.publisher.inplay.context.InplayMiddlewareContext
import com.oxygen.publisher.model.*
import com.oxygen.publisher.translator.AbstractWorker
import com.oxygen.publisher.translator.DiagnosticService
import groovy.util.logging.Slf4j
import retrofit2.Call
import retrofit2.Response
import spock.lang.Specification

import java.security.SecureRandom

import static com.oxygen.publisher.server.config.UnitTestUtil.fromFile

@Slf4j
class InplayChainFactorySpec extends Specification {

  InplayDataService inplayDataService
  InplayConsumerApi inplayConsumerApi = Mock()
  InplayServiceRegistry serviceRegistry = Mock()
  BroadcastOperations broadcastOperations = Mock()
  SocketIOServer ioServer = Mock()
  Call versionCall = Mock()
  Call inPlayModelCall = Mock()
  Call sportsRibbonCall = Mock()
  Call sportSegmentCall = Mock()
  Call inPlayCacheCall = Mock()
  Call virtualSportsCall = Mock()
  InplayMiddlewareContext middlewareContext

  InplayChainFactory chainFactory

  InplayCachedData cachedData

  String storageGenerationId = "1"
  private DiagnosticService diagnosticService
  private ObjectMapper objectMapper

  def setup() {
    InplayServiceConfiguration serviceConfiguration = Spy(InplayServiceConfiguration)

    inplayDataService = new InplayDataServiceImpl()
    inplayDataService.setServiceRegistry(serviceRegistry)
    serviceRegistry.getInplayDataService() >> inplayDataService
    serviceRegistry.getInplayConsumerApi() >> inplayConsumerApi
    serviceRegistry.getSocketIOServer() >> ioServer
    ioServer.getRoomOperations(_) >> broadcastOperations

    middlewareContext = serviceConfiguration.middlewareContext(serviceRegistry)

    cachedData = Mock()
    assert cachedData.getSportsRibbon() == null
    diagnosticService = Mock(DiagnosticService)
    objectMapper = new JsonSupportConfig().objectMapper()
    chainFactory = new InplayChainFactory(middlewareContext, this.diagnosticService, objectMapper)
    InplayChainFactory.setInplayChainFactory(chainFactory)
    inplayConsumerApi.getVersion() >> versionCall
    inplayConsumerApi.getInPlayModel(storageGenerationId) >> inPlayModelCall
    inplayConsumerApi.getSportsRibbon(storageGenerationId) >> sportsRibbonCall
    inplayConsumerApi.getSportSegment(storageGenerationId) >> sportSegmentCall
    inplayConsumerApi.getInPlayCache(storageGenerationId) >> inPlayCacheCall
    inplayConsumerApi.getVirtualSports(storageGenerationId) >> virtualSportsCall
  }

  def waitForUpdatedCache(String lockId) {
    synchronized (lockId.intern()) {
      log.info("Unlock.")
    }
  }

  def "Scheduled Job"() {

    given:
    versionCall.execute() >> Response.success(storageGenerationId)

    InPlayData inPlayData = fromFile("response/inplayData.json", InPlayData.class) // inplayDataChanged
    inPlayModelCall.execute() >> Response.success(inPlayData)

    List<VirtualSportEvents> virtualSportEvents = fromFile("response/virtualSports.json", List.class);
    virtualSportsCall.execute() >> Response.success(virtualSportEvents)

    SportsRibbon sportsRibbon = fromFile("storage/sportsRibbon.json", SportsRibbon.class) // sportsRibbon
    sportsRibbonCall.execute() >> Response.success(sportsRibbon)

    InPlayCache inPlayCache = fromFile("storage/InPlayCache.json", InPlayCache.class) // inplayCacheWorker
    inPlayCacheCall.execute() >> Response.success(inPlayCache)

    when:
    chainFactory.getScheduledJob().start(null)
    waitForUpdatedCache(storageGenerationId)

    then:
    0 * broadcastOperations.sendEvent("IN_PLAY_STRUCTURE_CHANGED", "data")
    null != middlewareContext.getInplayCachedData().getStructure()
    80 == middlewareContext.getInplayCachedData().getStructure().getLivenow().getEventsIds().size()
    5 == middlewareContext.getInplayCachedData().getStructure().getLivenow().getEventsBySports().size()
    3 == middlewareContext.getInplayCachedData().getStructure().getUpcoming().getEventsBySports().size()
    9 == middlewareContext.getInplayCachedData().getStructure().getUpcoming().getEventsIds().size()

    null != middlewareContext.getInplayCachedData().getSportsRibbon()
    7 == middlewareContext.getInplayCachedData().getSportsRibbon().getItems().size()

    !middlewareContext.getInplayCachedData().getSportSegments().isEmpty()
    69 == middlewareContext.getInplayCachedData().getSportSegments().size()
    4 == middlewareContext.getInplayCachedData().getSportSegments().get(new RawIndex("16::LIVE_EVENT::Match Betting::442")).getModuleDataItem().size()
    null != middlewareContext.getInplayCachedData().getSportSegments().get(new RawIndex("16::LIVE_EVENT")).getSportSegment()

  }

  def "Inplay Data Changed"() {
    given:
    InPlayData inPlayData = fromFile("response/inplayData.json", InPlayData.class) // inplayDataWorker  inplayDataChanged
    inPlayModelCall.execute() >> Response.success(inPlayData)

    SportsRibbon sportsRibbon = fromFile("storage/sportsRibbon.json", SportsRibbon.class) // sportsRibbon
    sportsRibbonCall.execute() >> Response.success(sportsRibbon)

    InPlayCache inPlayCache = fromFile("storage/InPlayCache.json", InPlayCache.class) // inplayCacheWorker
    inPlayCacheCall.execute() >> Response.success(inPlayCache)

    List<VirtualSportEvents> virtualSportEvents = fromFile("response/virtualSports.json", List.class);
    virtualSportsCall.execute() >> Response.success(virtualSportEvents)

    when:
    chainFactory.inplayDataChanged().start(storageGenerationId)
    waitForUpdatedCache(storageGenerationId)

    then:
    null != middlewareContext.getInplayCachedData().getStructure()
    80 == middlewareContext.getInplayCachedData().getStructure().getLivenow().getEventsIds().size()
    5 == middlewareContext.getInplayCachedData().getStructure().getLivenow().getEventsBySports().size()
    3 == middlewareContext.getInplayCachedData().getStructure().getUpcoming().getEventsBySports().size()
    9 == middlewareContext.getInplayCachedData().getStructure().getUpcoming().getEventsIds().size()

    null != middlewareContext.getInplayCachedData().getSportsRibbon()
    7 == middlewareContext.getInplayCachedData().getSportsRibbon().getItems().size()

    !middlewareContext.getInplayCachedData().getSportSegments().isEmpty()
    69 == middlewareContext.getInplayCachedData().getSportSegments().size()
    4 == middlewareContext.getInplayCachedData().getSportSegments().get(new RawIndex("16::LIVE_EVENT::Match Betting::442")).getModuleDataItem().size()
    null != middlewareContext.getInplayCachedData().getSportSegments().get(new RawIndex("16::LIVE_EVENT")).getSportSegment()

    1 * broadcastOperations.sendEvent("IN_PLAY_STRUCTURE_CHANGED", _ as Object)
    0 * broadcastOperations.sendEvent("IN_PLAY_SPORTS_RIBBON_CHANGED", _ as Object)

  }

  def "Sport Ribbon Changed"() {

    given:
    SportsRibbon sportsRibbon = fromFile("storage/sportsRibbon.json", SportsRibbon.class) // sportsRibbon
    sportsRibbonCall.execute() >> Response.success(sportsRibbon)

    InPlayData emptyInplayData = new InPlayData()
    middlewareContext.getInplayCachedData().setStructureWithoutStreamEvents(emptyInplayData)
    AbstractWorker thisWorker = chainFactory.sportsRibbonChanged()

    when:
    thisWorker.start(storageGenerationId)
    waitForUpdatedCache(thisWorker.getChainId())

    then:
    emptyInplayData == middlewareContext.getInplayCachedData().getStructureWithoutStreamEvents()

    null != middlewareContext.getInplayCachedData().getSportsRibbon()
    7 == middlewareContext.getInplayCachedData().getSportsRibbon().getItems().size()

    null != middlewareContext.getInplayCachedData().getSportsRibbonWithLiveStreams()
    5 == middlewareContext.getInplayCachedData().getSportsRibbonWithLiveStreams().getItems().size()

    middlewareContext.getInplayCachedData().getSportSegments().isEmpty()

    1 * broadcastOperations.sendEvent("IN_PLAY_SPORTS_RIBBON_CHANGED", _ as Object)
    1 * broadcastOperations.sendEvent("IN_PLAY_LS_SPORTS_RIBBON_CHANGED", _ as Object)
    0 * broadcastOperations.sendEvent("IN_PLAY_STRUCTURE_CHANGED", _ as Object)
    0 * broadcastOperations.sendEvent("IN_PLAY_LS_STRUCTURE_CHANGED", _ as Object)
  }

  def "Sport Segment Changed"() {

    given:
    SportSegment sportSegment = fromFile("storage/SportSegment.json", SportSegment.class) // sportSegmentsChanged
    sportSegmentCall.execute() >> Response.success(sportSegment)

    InplayCachedData thisLock = new InplayCachedData()
    thisLock.setVersion(storageGenerationId)

    when:
    chainFactory.onSportSegmentsChanged().start(storageGenerationId)
    waitForUpdatedCache(thisLock.getVersion())

    then:
    null == middlewareContext.getInplayCachedData().getStructure()
    null == middlewareContext.getInplayCachedData().getSportsRibbon()
    !middlewareContext.getInplayCachedData().getSportSegments().isEmpty()
    7 == middlewareContext.getInplayCachedData().getSportSegments().size()
    4 == middlewareContext.getInplayCachedData().getSportSegments().get(new RawIndex("16::LIVE_EVENT::Match Betting::442")).getModuleDataItem().size()
    null != middlewareContext.getInplayCachedData().getSportSegments().get(new RawIndex("16::LIVE_EVENT::Match Betting")).getSportSegment()

    broadcastOperations.sendEvent(_ as String, _ as Object)
  }

  def "Virtual Sports Ribbon Changed"() {
    given:

    List<VirtualSportEvents> virtualSportEvents = fromFile("response/virtualSports.json", List.class);
    virtualSportsCall.execute() >> Response.success(virtualSportEvents)
    InPlayData emptyInplayData = new InPlayData()
    middlewareContext.getInplayCachedData().setStructure(emptyInplayData)
    emptyInplayData.setVirtualSportList(virtualSportEvents)

    AbstractWorker thisWorker = chainFactory.virtualSportsRibbonChanged();

    when:
    thisWorker.start(storageGenerationId)
    waitForUpdatedCache(thisWorker.getChainId())

    then:

    null != middlewareContext.getInplayCachedData().getStructure().getVirtualSportList()


    0 * broadcastOperations.sendEvent("GET_VIRTUAL_SPORTS_RIBBON_REQUEST", _ as Object)
    1 * broadcastOperations.sendEvent("GET_VIRTUAL_SPORTS_RIBBON_RESPONSE", _ as Object)
  }


  def "Reset event market"() {
    given:
    InPlayCache inPlayCache = fromFile("storage/InPlayCache.json", InPlayCache.class)
    SportSegment sportSegment = fromFile("storage/SportSegment.json", SportSegment.class)
    InPlayByEventMarket eventMarket = new InPlayByEventMarket()
    ModuleDataItem moduleDataItem = new ModuleDataItem()
    moduleDataItem.setName("Test")
    moduleDataItem.setId(123)
    eventMarket.setModuleDataItem(moduleDataItem)
    RawIndex index = new RawIndex(sportSegment)
    Map<RawIndex, InPlayCache.SportSegmentCache> cacheMap = new HashMap<RawIndex, InPlayCache.SportSegmentCache>()
    cacheMap.put(index, inPlayCache.getSportSegmentCaches().get(0))
    ModuleDataItem oldModuleDataItem = inPlayCache.getSportSegmentCaches().get(0).getModuleDataItem().get(0)

    when:
    chainFactory.resetEventMarket(eventMarket, index, cacheMap, oldModuleDataItem)

    then:
    inPlayCache.getSportSegmentCaches().get(0).getModuleDataItem().get(0).getName() == "Test"
    inPlayCache.getSportSegmentCaches().get(0).getModuleDataItem().get(0).getId() == 123
  }

  def "Reset event market - IAOB"() {
    given:
    InPlayCache inPlayCache = fromFile("storage/InPlayCache.json", InPlayCache.class)
    SportSegment sportSegment = fromFile("storage/SportSegment.json", SportSegment.class)
    InPlayByEventMarket eventMarket = new InPlayByEventMarket()
    ModuleDataItem moduleDataItem = new ModuleDataItem()
    moduleDataItem.setName("Test")
    moduleDataItem.setId(123)
    eventMarket.setModuleDataItem(moduleDataItem)
    RawIndex index = new RawIndex(sportSegment)
    Map<RawIndex, InPlayCache.SportSegmentCache> cacheMap = new HashMap<RawIndex, InPlayCache.SportSegmentCache>()
    cacheMap.put(index, inPlayCache.getSportSegmentCaches().get(0))
    ModuleDataItem oldModuleDataItem = new ModuleDataItem()
    oldModuleDataItem.setName("Test2")
    oldModuleDataItem.setId(4567)

    when:
    chainFactory.resetEventMarket(eventMarket, index, cacheMap, oldModuleDataItem)

    then:
    inPlayCache.getSportSegmentCaches().get(0).getModuleDataItem().get(0).getName() != "Test"
    inPlayCache.getSportSegmentCaches().get(0).getModuleDataItem().get(0).getId() != 123
  }

  def "sports competition updated"(){
    given:
    String sportCompetitionChange = fromFile( "storage/InplaySportCompetitionChange.json")
    InPlayCache inPlayCache = fromFile("storage/InPlayCache.json", InPlayCache.class) // inplayCacheWorker
    inPlayCacheCall.execute() >> Response.success(inPlayCache)

    when:
    chainFactory.processCompetitionChanges().start(sportCompetitionChange)

    then:
    1 * broadcastOperations.sendEvent("IN_PLAY_SPORT_COMPETITION_CHANGED::16::LIVE_EVENT", _ as Object)


  }

  def "reflect EVMKT live updates no other PR markets"(){
    given:
    def eventId = "12335"
    def marketId = "15"
    BaseObject liveUpdate = createLiveUpdate("EVMKT", eventId, marketId, "N")
    InPlayByEventMarket inPlayByMarket = createInplayEventMarketItem(marketId, Collections.emptyList())
    middlewareContext.getInplayCachedData().getPrimaryMarketCache()
        .put(eventId+ "::"+ marketId, inPlayByMarket);

    when:
    chainFactory.reflectLiveUpdates(eventId).start(liveUpdate)

    then:
    middlewareContext.getInplayCachedData().getPrimaryMarketCache().size() == 1
  }

  def "process live updates"(){
    given:
    def eventId = "12335"
    def marketId1 = "15"
    def marketId2 = "27"
    BaseObject liveUpdate = createLiveUpdate("EVMKT", eventId, marketId1, "N")
    def primaryMarkets = Arrays.asList(createMarket(marketId1), createMarket(marketId2))
    InPlayByEventMarket inPlayByMarket1 = createInplayEventMarketItem(marketId1, primaryMarkets)
    middlewareContext.getInplayCachedData().getPrimaryMarketCache()
        .put(eventId+ "::"+ marketId1, inPlayByMarket1);

    InPlayByEventMarket inPlayByMarket2 = createInplayEventMarketItem(marketId2, primaryMarkets)
    middlewareContext.getInplayCachedData().getPrimaryMarketCache()
        .put(eventId+ "::"+ marketId2, inPlayByMarket2);

    when:
    chainFactory.processLiveUpdate(eventId, objectMapper.writeValueAsString(liveUpdate))

    then:
    1 * ioServer.getRoomOperations(eventId) >> broadcastOperations
    1 * broadcastOperations.sendEvent(eventId, [liveUpdate])
    middlewareContext.getInplayCachedData().getPrimaryMarketCache().size() == 2
  }

  private static InPlayByEventMarket createInplayEventMarketItem(String marketId, List<OutputMarket> primaryMarkets) {
    def dataItem = new ModuleDataItem()
    dataItem.setMarkets(Collections.singletonList(createMarket(marketId)))

    def inPlayByMarket = new InPlayByEventMarket()
    inPlayByMarket.setModuleDataItem(dataItem)
    inPlayByMarket.setPrimaryMarkets(primaryMarkets)
    inPlayByMarket.addCacheRef(
        RawIndex.builder()
        .categoryId(16)
        .typeId(111)
        .topLevelType("LIVE_EVENT")
        .build())
    inPlayByMarket
  }

  private static OutputMarket createMarket(String marketId) {
    def market = new OutputMarket()
    market.setId(marketId)
    market
  }

  private static BaseObject createLiveUpdate(String type, String eventId, String marketId, String isDisplayed) {
    def event = new BaseObject.Event()
    event.setEventId(Integer.parseInt(eventId))
    def market = new BaseObject.Market()
    market.setMarketId(Integer.parseInt(marketId))
    market.setDisplayed(isDisplayed)
    market.setStatus("A")
    event.setMarket(market)
    BaseObject liveUpdate = new BaseObject()
    liveUpdate.setType(type)
    liveUpdate.setEvent(event)
    liveUpdate
  }
}
