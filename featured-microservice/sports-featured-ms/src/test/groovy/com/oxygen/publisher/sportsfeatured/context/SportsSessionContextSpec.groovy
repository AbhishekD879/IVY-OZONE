package com.oxygen.publisher.sportsfeatured.context

import com.corundumstudio.socketio.AckRequest
import com.corundumstudio.socketio.HandshakeData
import com.corundumstudio.socketio.SocketIOClient
import com.oxygen.publisher.SocketIoTestHelper
import com.oxygen.publisher.model.ApplicationVersion
import com.oxygen.publisher.model.OutputMarket
import com.oxygen.publisher.sportsfeatured.model.FeaturedModel
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData
import com.oxygen.publisher.sportsfeatured.model.module.*
import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData
import com.oxygen.publisher.sportsfeatured.model.module.data.FanBetsConfig
import com.oxygen.publisher.sportsfeatured.model.module.data.PopularBetModuleData
import com.oxygen.publisher.sportsfeatured.model.module.data.QuickLinkData
import com.oxygen.publisher.sportsfeatured.model.module.data.SurfaceBetModuleData
import com.oxygen.publisher.sportsfeatured.model.module.data.TeamBetsConfig
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.SportSegment
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.TypeSegment
import spock.lang.Specification

import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

class SportsSessionContextSpec extends Specification {

  SportsSessionContext sportsSessionContext
  SportsMiddlewareContext middlewareContext
  SportsCachedData sportsCachedData
  SocketIOClient client

  void setup() {
    middlewareContext = Mock()
    sportsCachedData = Mock()
    middlewareContext.getFeaturedCachedData() >> sportsCachedData
    client = Mock()

    client.getHandshakeData() >> Mock(HandshakeData)
    client.getSessionId() >> UUID.randomUUID()

    sportsSessionContext = new SportsSessionContext(new ApplicationVersion("v.1.2"), middlewareContext)
  }

  def "OnConnect join InternationalToteModule"() {
    client.getHandshakeData().getSingleUrlParam("sportId") >> "16"
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("16#FEATURED_STRUCTURE_CHANGED")
    given:
    def toteModule = createInternationalToteModule("123457")
    CountDownLatch latch = new CountDownLatch(1)

    when:
    sportsSessionContext.onConnect(client)
    latch.await(10, TimeUnit.SECONDS)

    then:
    1 * sportsCachedData.getStructure(_) >> createStructure("13",toteModule)
    1 * client.joinRoom(toteModule.getSportId()+ "#" +toteModule.getId()) >> { args -> latch.countDown() }
  }

  def "OnConnect join InternationalToteModuleWithUseFscCacheEnabled"() {
    client.getHandshakeData().getSingleUrlParam("sportId") >> "16"
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("16#FEATURED_STRUCTURE_CHANGED")
    given:
    def toteModule = createInternationalToteModule("123457")
    CountDownLatch latch = new CountDownLatch(1)
    FeaturedModel model = createStructure("16",toteModule)
    model.setUseFSCCached(true)

    when:
    sportsSessionContext.onConnect(client)
    latch.await(1, TimeUnit.SECONDS)

    then:
    1 * sportsCachedData.getStructure(_) >> model
    1 * client.joinRoom( "0#"+toteModule.getId()) >> { args -> latch.countDown() }
  }

  def "OnConnect join withNoStructure"() {
    client.getHandshakeData().getSingleUrlParam("sportId") >> "0"
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("0#FEATURED_STRUCTURE_CHANGED")
    given:
    def CountDownLatch latch = new CountDownLatch(1)

    when:
    sportsSessionContext.onConnect(client)
    latch.await(1, TimeUnit.SECONDS)
    then:
    1 * sportsCachedData.getStructure(_) >> null
  }

  def "OnConnect join withSegmentwiseModules"() {
    client.getHandshakeData().getSingleUrlParam("sportId") >> "16"
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("0#FEATURED_STRUCTURE_CHANGED")
    given:
    def CountDownLatch latch = new CountDownLatch(1)

    when:
    sportsSessionContext.onConnect(client)
    latch.await(1, TimeUnit.SECONDS)

    then:
    1 * sportsCachedData.getStructure(_) >> createStructureWithSegmentWiseModules("16")
  }

  def "OnConnect join withFanzoneSegmentwiseModules"() {
    client.getHandshakeData().getSingleUrlParam("sportId") >> "160"
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("160#FEATURED_STRUCTURE_CHANGED")
    given:
    def CountDownLatch latch = new CountDownLatch(1)

    when:
    sportsSessionContext.onConnect(client)
    latch.await(1, TimeUnit.SECONDS)

    then:
    0 * sportsCachedData.getStructure(_) >> createStructureWithFanzoneSegmentWiseModules("160")
  }

  def "OnConnect join withSegmentwiseModulesNoSegmentView"() {
    client.getHandshakeData().getSingleUrlParam("sportId") >> "0"
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("0#FEATURED_STRUCTURE_CHANGED")
    given:
    def CountDownLatch latch = new CountDownLatch(1)
    FeaturedModel model = createStructureWithSegmentWiseModules("0")
    Map<String, SegmentView> segmentWiseModules = model.getSegmentWiseModules()
    segmentWiseModules.remove("Universal")
    model.setSegmentWiseModules(segmentWiseModules)

    when:
    sportsSessionContext.onConnect(client)
    latch.await(1, TimeUnit.SECONDS)

    then:
    1 * sportsCachedData.getStructure(_) >> model
  }

  def "OnConnect join withFanzoneSegmentwiseModulesNoFanzoneSegmentView"() {
    client.getHandshakeData().getSingleUrlParam("sportId") >> "160"
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("160#FEATURED_STRUCTURE_CHANGED")
    given:
    def CountDownLatch latch = new CountDownLatch(1)
    FeaturedModel model = createStructureWithFanzoneSegmentWiseModules("160")
    Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules = model.getFanzoneSegmentWiseModules()
    fanzoneSegmentWiseModules.remove("Universal")
    model.setFanzoneSegmentWiseModules(fanzoneSegmentWiseModules)

    when:
    sportsSessionContext.onConnect(client)
    latch.await(1, TimeUnit.SECONDS)

    then:
    0 * sportsCachedData.getStructure(_) >> model
  }

  def "OnConnect join withEmptySegmentwiseModules"() {
    client.getHandshakeData().getSingleUrlParam("sportId") >> "0"
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("0#FEATURED_STRUCTURE_CHANGED")
    given:
    def SurfaceBetModule surfaceBetModule = createSurfaceBetModule("surfaceBet Link")
    CountDownLatch latch = new CountDownLatch(1)
    FeaturedModel model = createStructure("0",surfaceBetModule)
    model.setSegmentWiseModules(null)
    model.setUseFSCCached(true)

    when:
    sportsSessionContext.onConnect(client)
    latch.await(1, TimeUnit.SECONDS)

    then:
    1 * sportsCachedData.getStructure(_) >> model
  }


  def "OnConnect join withEmptyFanzoneSegmentwiseModules"() {
    client.getHandshakeData().getSingleUrlParam("sportId") >> "160"
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("160#FEATURED_STRUCTURE_CHANGED")
    given:
    def SurfaceBetModule surfaceBetModule = createFanzoneSurfaceBetModule("surfaceBet Link")
    CountDownLatch latch = new CountDownLatch(1)
    FeaturedModel model = createStructure("160",surfaceBetModule)
    model.setFanzoneSegmentWiseModules(null)

    when:
    sportsSessionContext.onConnect(client)
    latch.await(1, TimeUnit.SECONDS)

    then:
    0 * sportsCachedData.getStructure(_) >> model
  }

  def "OnLogin join withEmptySegment"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("0#FEATURED_STRUCTURE_CHANGED")
    given:
    CountDownLatch latch = new CountDownLatch(1)

    when:
    sportsSessionContext.onLogin(client,"0#")
    latch.await(1, TimeUnit.SECONDS)
    then:
    1 * sportsCachedData.getStructure(_) >> createStructureWithSegmentWiseModules("0")
  }

  def "OnLogin join withEmptyFanzoneSegment"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("160#FEATURED_STRUCTURE_CHANGED")
    given:
    def CountDownLatch latch = new CountDownLatch(1)

    when:
    sportsSessionContext.onLogin(client,null)
    latch.await(1, TimeUnit.SECONDS)
    then:
    thrown(IllegalArgumentException)
  }

  def "OnLogin join withSegment"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("0#FEATURED_STRUCTURE_CHANGED")
    client.getAllRooms() >> Arrays.asList("0#room1")
    given:
    def CountDownLatch latch = new CountDownLatch(1)

    when:
    sportsSessionContext.onLogin(client,"0#segment-one")
    latch.await(1, TimeUnit.SECONDS)
    then:
    1 * sportsCachedData.getStructure(_) >> createStructureWithSegmentWiseModules("0")
  }

  def "OnLogin join withFanzoneSegment"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("160#FEATURED_STRUCTURE_CHANGED")
    client.getAllRooms() >> Arrays.asList("160#room1")
    given:
    def CountDownLatch latch = new CountDownLatch(1)

    when:
    sportsSessionContext.onLogin(client,"160#segment-one")
    latch.await(1, TimeUnit.SECONDS)
    then:
    1 * sportsCachedData.getStructure(_) >> createStructureWithFanzoneSegmentWiseModules("160")
  }
  def "OnLogin join withFanzoneSegment When fanzoneSegmentView  is null"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("160#FEATURED_STRUCTURE_CHANGED")
    client.getAllRooms() >> Arrays.asList("160#room1")
    given:
    def CountDownLatch latch = new CountDownLatch(1)
    when:
    sportsSessionContext.onLogin(client,"160#null-segment")
    latch.await(1, TimeUnit.SECONDS)
    then:
    1 * sportsCachedData.getStructure(_) >> createStructureWithFanzoneSegmentWiseModules("160")
  }
  def "OnLogin join withSegmentAndNoStructure"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("0#FEATURED_STRUCTURE_CHANGED")
    client.getAllRooms() >> Arrays.asList("0#room1")
    given:
    def CountDownLatch latch = new CountDownLatch(1)

    when:
    sportsSessionContext.onLogin(client,"0#segment-one")
    latch.await(1, TimeUnit.SECONDS)
    then:
    1 * sportsCachedData.getStructure(_) >> null
  }

  def "OnLogin join withFanzoneSegmentAndNoStructure"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("160#FEATURED_STRUCTURE_CHANGED")
    client.getAllRooms() >> Arrays.asList("160#room1")
    given:
    def CountDownLatch latch = new CountDownLatch(1)

    when:
    sportsSessionContext.onLogin(client,"160#segment-one")
    latch.await(1, TimeUnit.SECONDS)
    then:
    1 * sportsCachedData.getStructure(_) >> null
  }

  def "OnLogin join withSegmentWithNoSegmentWiseModules"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("0#FEATURED_STRUCTURE_CHANGED")
    client.getAllRooms() >> Arrays.asList("0#room1")
    given:
    def CountDownLatch latch = new CountDownLatch(1)
    FeaturedModel featuredModel = createStructureWithSegmentWiseModules("0")
    featuredModel.setSegmentWiseModules(null)

    when:
    sportsSessionContext.onLogin(client,"0#segment-one")
    latch.await(1, TimeUnit.SECONDS)
    then:
    1 * sportsCachedData.getStructure(_) >> featuredModel
  }

  def "OnLogin join withFanzoneSegmentWithNoFanzoneSegmentWiseModules"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("0#FEATURED_STRUCTURE_CHANGED")
    client.getAllRooms() >> Arrays.asList("0#room1")
    given:
    def CountDownLatch latch = new CountDownLatch(1)
    FeaturedModel featuredModel = createNoStructureWithNoFanzoneSegmentWiseModules("160")
    featuredModel.setFanzoneSegmentWiseModules(null)
    when:
    sportsSessionContext.onLogin(client,"0#segment-one")
    latch.await(1, TimeUnit.SECONDS)
    then:
    2 * sportsCachedData.getStructure(_) >> featuredModel
  }

  def "OnLogin join withFanzoneSegmentWithNoSurfaceBetModules"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("160#FEATURED_STRUCTURE_CHANGED")
    client.getAllRooms() >> Arrays.asList("160#room1")
    given:
    def CountDownLatch latch = new CountDownLatch(1)
    FeaturedModel featuredModel = createStructureWithFanzoneSegmentWiseModulesNoSurfaceBet("160")

    when:
    sportsSessionContext.onLogin(client,"160#segment-one")
    latch.await(1, TimeUnit.SECONDS)
    then:
    1 * sportsCachedData.getStructure(_) >> featuredModel
  }

  def "OnLogin join withFanzoneSegmentWithNoMatchingTeamExtId"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("160#FEATURED_STRUCTURE_CHANGED")
    client.getAllRooms() >> Arrays.asList("160#room1")
    given:
    def CountDownLatch latch = new CountDownLatch(1)
    FeaturedModel featuredModel = createStructureWithFanzoneSegmentWiseModulesNoMatchingEventName("160")

    when:
    sportsSessionContext.onLogin(client,"160#segment-one")
    latch.await(1, TimeUnit.SECONDS)
    then:
    1 * sportsCachedData.getStructure(_) >> featuredModel
  }

  def "OnLogin join withNoMatchingSegmentToSendData"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("0#FEATURED_STRUCTURE_CHANGED")
    client.getAllRooms() >> Arrays.asList("room1")
    given:
    def CountDownLatch latch = new CountDownLatch(1)

    when:
    sportsSessionContext.onLogin(client,"0#segment-two")
    latch.await(1, TimeUnit.SECONDS)
    then:
    2 * sportsCachedData.getStructure(_) >> createStructureWithSegmentWiseModules("0")
  }

  def "OnSubscribe withSegmentUniversal"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("0#moduleId")
    given:
    def CountDownLatch latch = new CountDownLatch(1)
    EventsModule eventsModule = createFeaturedModule("FeatureModule")
    eventsModule.setSegmented(true)
    Map<String, SegmentView> moduleSegmentView = new HashMap()
    SegmentView segmentView = new SegmentView()
    SegmentOrderdModule segmentOrderdModuleForEventModule = new SegmentOrderdModule(1, eventsModule)
    List<EventsModuleData> eventsModuleDataList = new ArrayList<>()
    EventsModuleData eventsModuleData = new EventsModuleData()
    eventsModuleDataList.add(eventsModuleData)
    segmentOrderdModuleForEventModule.setEventsModuleData(eventsModuleDataList)
    segmentView.getEventModules().put(eventsModule.getId(), segmentOrderdModuleForEventModule)
    moduleSegmentView.put("Universal", segmentView)
    eventsModule.setModuleSegmentView(moduleSegmentView)

    List<String> rooms = new ArrayList<>()
    rooms.add("0#FeatureModule");

    when:
    sportsSessionContext.onSubscribe(client,rooms)
    latch.await(1, TimeUnit.SECONDS)

    then:
    1 * sportsCachedData.getModuleIfPresent(_) >> eventsModule
  }

  def "OnSubscribe withSegment"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("0#moduleId")
    given:
    def CountDownLatch latch = new CountDownLatch(1)
    EventsModule eventsModule = createFeaturedModule("FeatureModule")
    eventsModule.setSegmented(true)
    Map<String, SegmentView> moduleSegmentView = new HashMap()
    SegmentView segmentView = new SegmentView()
    SegmentOrderdModule segmentOrderdModuleForEventModule = new SegmentOrderdModule(1, eventsModule)
    List<EventsModuleData> eventsModuleDataList = new ArrayList<>()
    EventsModuleData eventsModuleData = new EventsModuleData()
    eventsModuleDataList.add(eventsModuleData)
    segmentOrderdModuleForEventModule.setEventsModuleData(eventsModuleDataList)
    segmentView.getEventModules().put(eventsModule.getId(), segmentOrderdModuleForEventModule)
    moduleSegmentView.put("segment", segmentView)
    eventsModule.setModuleSegmentView(moduleSegmentView)

    List<String> rooms = new ArrayList<>()
    rooms.add("0#FeatureModule#segment");

    when:
    sportsSessionContext.onSubscribe(client,rooms)
    latch.await(1, TimeUnit.SECONDS)

    then:
    1 * sportsCachedData.getModuleIfPresent(_) >> eventsModule
  }

  def "OnSubscribe nonSegmentedEventModule"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("0#moduleId")
    given:
    def CountDownLatch latch = new CountDownLatch(1)
    EventsModule eventsModule = createFeaturedModule("FeatureModule")
    eventsModule.setSegmented(false)
    eventsModule.setModuleSegmentView(new HashMap<String, SegmentView>());

    List<String> rooms = new ArrayList<>()
    rooms.add("0#FeatureModule");

    when:
    sportsSessionContext.onSubscribe(client,rooms)
    latch.await(1, TimeUnit.SECONDS)

    then:
    1 * sportsCachedData.getModuleIfPresent(_) >> eventsModule
  }

  def "OnSubscribe segmentedInplayModule"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("0#moduleId")
    given:
    def CountDownLatch latch = new CountDownLatch(1)
    InplayModule inplayModule = createInplayModule("InplayModule")
    inplayModule.setSegmented(true)
    inplayModule.setModuleSegmentView(new HashMap<String, SegmentView>());

    List<String> rooms = new ArrayList<>()
    rooms.add("0#FeatureModule");

    when:
    sportsSessionContext.onSubscribe(client,rooms)
    latch.await(1, TimeUnit.SECONDS)

    then:
    1 * sportsCachedData.getModuleIfPresent(_) >> inplayModule
  }
  def "OnSubscribe segmentNotInModuleSegmentView"() {
    sportsCachedData.getSportPageData() >> SocketIoTestHelper.sportPageMapCache
    client.getAllRooms() >>List.of("0#moduleId")
    given:
    def CountDownLatch latch = new CountDownLatch(1)
    EventsModule eventsModule = createFeaturedModule("FeatureModule")
    eventsModule.setSegmented(true)
    Map<String, SegmentView> moduleSegmentView = new HashMap()
    SegmentView segmentView = new SegmentView()
    SegmentOrderdModule segmentOrderdModuleForEventModule = new SegmentOrderdModule(1, eventsModule)
    List<EventsModuleData> eventsModuleDataList = new ArrayList<>()
    EventsModuleData eventsModuleData = new EventsModuleData()
    eventsModuleDataList.add(eventsModuleData)
    segmentOrderdModuleForEventModule.setEventsModuleData(eventsModuleDataList)
    segmentView.getEventModules().put(eventsModule.getId(), segmentOrderdModuleForEventModule)
    moduleSegmentView.put("segment", segmentView)
    eventsModule.setModuleSegmentView(moduleSegmentView)

    List<String> rooms = new ArrayList<>()
    rooms.add("0#12345");

    when:
    sportsSessionContext.onSubscribe(client,rooms)
    latch.await(1, TimeUnit.SECONDS)

    then:
    1 * sportsCachedData.getModuleIfPresent(_) >> eventsModule
  }

  def "OnSubscribe without modules"() {
    given:
    CountDownLatch latch = new CountDownLatch(1)
    InplayModule inplayModule = createInplayModule(null)
    inplayModule.setSegmented(true)

    when:
    sportsSessionContext.onSubscribe(client,null)
    latch.await(1, TimeUnit.SECONDS)

    then:
    inplayModule.getId() == null
  }

  def "OnSubscribe with modules empty"() {
    given:
    CountDownLatch latch = new CountDownLatch(1)
    InplayModule inplayModule = createInplayModule(null)
    inplayModule.setSegmented(true)

    List<String> rooms = new ArrayList<>()
    when:
    sportsSessionContext.onSubscribe(client,rooms)
    latch.await(1, TimeUnit.SECONDS)

    then:
    inplayModule.getId() == null
  }

  def "OnSubscribe without module"() {
    given:
    CountDownLatch latch = new CountDownLatch(1)
    InplayModule inplayModule = createInplayModule(null)
    inplayModule.setSegmented(true)
    AckRequest request = Mock()

    when:
    sportsSessionContext.onSubscribe(client,null, request)
    latch.await(1, TimeUnit.SECONDS)

    then:
    inplayModule.getId() == null
  }

  def "OnSubscribe with module hash"() {
    given:
    CountDownLatch latch = new CountDownLatch(1)
    InplayModule inplayModule = createInplayModule(null)
    inplayModule.setSegmented(true)
    AckRequest request = Mock()

    when:
    sportsSessionContext.onSubscribe(client,"16", request)
    latch.await(1, TimeUnit.SECONDS)

    then:
    inplayModule.getId() == null
  }

  FeaturedModel createStructure(String pageId,AbstractFeaturedModule...modules) {
    FeaturedModel model = new FeaturedModel(pageId)
    Arrays.stream(modules).forEach({ m -> model.addModule(m) })
    model
  }

  FeaturedModel createStructureWithSegmentWiseModules(String pageId) {
    FeaturedModel model = new FeaturedModel(pageId)
    model.addModule(createInternationalToteModule("Tote Module"))
    Map<String, SegmentView> segmentWiseModules = new HashMap<>()
    SegmentView segmentView = new SegmentView()
    HighlightCarouselModule highlightCarouselModule = createHighlightCarouselModule("Highlight Carousel")
    model.addModule(highlightCarouselModule)
    SegmentOrderdModule segmentOrderdModuleForHc = new SegmentOrderdModule(1, highlightCarouselModule)
    segmentView.getHighlightCarouselModules().put(highlightCarouselModule.getId(), segmentOrderdModuleForHc)

    EventsModule featureModule =  createFeaturedModule("Feature Module")
    model.addModule(featureModule)
    SegmentOrderdModule segmentOrderdModuleForEventModule = new SegmentOrderdModule(1, featureModule)
    segmentView.getEventModules().put(featureModule.getId(), segmentOrderdModuleForEventModule)

    PopularBetModule popularBetModule =  createPopularBetModule()
    model.addModule(popularBetModule)
    SegmentOrderdModule segmentOrderdModuleForPopularModule = new SegmentOrderdModule(1, popularBetModule)
    segmentView.getEventModules().put(popularBetModule.getId(), segmentOrderdModuleForPopularModule)

    EventsModule featureModule2 =  createFeaturedModule("Feature Module 2")
    featureModule2.setShowExpanded(true)
    model.addModule(featureModule2)
    SegmentOrderdModule segmentOrderdModuleForEventModule2 = new SegmentOrderdModule(1, featureModule2)
    List<EventsModuleData> eventsModuleDataList2 = new ArrayList<>()
    EventsModuleData eventsModuleData2 = new EventsModuleData()
    eventsModuleDataList2.add(eventsModuleData2)
    segmentOrderdModuleForEventModule2.setEventsModuleData(eventsModuleDataList2)
    segmentView.getEventModules().put(featureModule2.getId(), segmentOrderdModuleForEventModule2)

    QuickLinkModule quickLinkModule = createQuickLinkModule("Quick Link")
    model.addModule(quickLinkModule)
    model.setQuickLinkModule(quickLinkModule)
    SegmentOrderdModuleData segmentOrderdModuleForQl = new SegmentOrderdModuleData(1, quickLinkModule.getData().get(0))
    segmentView.getQuickLinkData().put(quickLinkModule.getId(), segmentOrderdModuleForQl)

    SurfaceBetModule surfaceBetModule = createSurfaceBetModule("surfaceBet Link")
    model.addModule(surfaceBetModule)
    model.setSurfaceBetModule(surfaceBetModule)
    SegmentOrderdModuleData segmentOrderdModuleForSb = new SegmentOrderdModuleData(1, surfaceBetModule.getData().get(0))
    segmentView.getSurfaceBetModuleData().put(surfaceBetModule.getId(), segmentOrderdModuleForSb)

    InplayModule inplayModule = createInplayModule("Inplay Module")
    model.addModule(inplayModule)
    model.setInplayModule(inplayModule)
    SegmentOrderdModuleData segmentOrderdModuleForInplay = new SegmentOrderdModuleData(1, inplayModule.getData().get(0))
    List<SegmentedEvents> limitedEvents = new ArrayList<>()
    SegmentedEvents segmentedEvents = new SegmentedEvents()
    TypeSegment eventByTypeName = new TypeSegment()
    EventsModuleData eventsModuleData = new EventsModuleData()
    List<EventsModuleData> events = new ArrayList<>()
    events.add(eventsModuleData)
    segmentedEvents.setEventByTypeName(eventByTypeName)
    segmentedEvents.setEvents(events)
    limitedEvents.add(segmentedEvents)
    segmentOrderdModuleForInplay.setLimitedEvents(limitedEvents)
    segmentView.getInplayModuleData().put(inplayModule.getId(), segmentOrderdModuleForInplay)

    segmentWiseModules.put("Universal", segmentView)
    segmentWiseModules.put("segment-one", segmentView)
    model.setSegmentWiseModules(segmentWiseModules)
    model
  }

  FeaturedModel createStructureWithFanzoneSegmentWiseModules(String pageId) {
    FeaturedModel model = new FeaturedModel(pageId)
    Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules = new HashMap<>()
    FanzoneSegmentView fanzoneSegmentView = new FanzoneSegmentView()

    HighlightCarouselModule highlightCarouselModule = createFanzoneHighlightCarouselModule("Highlight Carousel")
    model.addModule(highlightCarouselModule)
    fanzoneSegmentView.getHighlightCarouselModules().put(highlightCarouselModule.getId(), highlightCarouselModule)

    HighlightCarouselModule highlightCarouselModule1 = createFanzoneHighlightCarouselModuleWithNoTeamExtIds("Highlight Carousel1")
    model.addModule(highlightCarouselModule1)
    fanzoneSegmentView.getHighlightCarouselModules().put(highlightCarouselModule1.getId(), highlightCarouselModule1)

    HighlightCarouselModule highlightCarouselModule2 = createFanzoneHighlightCarouselModuleWithNoTeamExtIds1("Highlight Carousel2")
    model.addModule(highlightCarouselModule2)
    fanzoneSegmentView.getHighlightCarouselModules().put(highlightCarouselModule2.getId(), highlightCarouselModule2)

    SurfaceBetModule surfaceBetModule = createFanzoneSurfaceBetModule("surfaceBet Link")
    model.addModule(surfaceBetModule)
    model.setSurfaceBetModule(surfaceBetModule)
    fanzoneSegmentView.getSurfaceBetModuleData().put(surfaceBetModule.getId(), surfaceBetModule.getData().get(0))


    TeamBetsModule teamBetsModule = createTeamBetsModule("Bets Based on Your Team")
    model.addModule(teamBetsModule)
    model.setTeamBetsModule(teamBetsModule)
    fanzoneSegmentView.getTeamBetsModuleData().put(teamBetsModule.getId(),teamBetsModule.getData().get(0))

    FanBetsModule fanBetsModule = createFanBetsModule("Bets Based on Other Fans")
    model.addModule(fanBetsModule)
    model.setFanBetsModule(fanBetsModule)
    fanzoneSegmentView.getFanBetsModuleData().put(fanBetsModule.getId(),fanBetsModule.getData().get(0))

    fanzoneSegmentWiseModules.put("Universal", fanzoneSegmentView)
    fanzoneSegmentWiseModules.put("segment-one", fanzoneSegmentView)
    fanzoneSegmentWiseModules.put("null-segment", null )
    model.setFanzoneSegmentWiseModules(fanzoneSegmentWiseModules)
    model
  }

  FeaturedModel createStructureWithFanzoneSegmentWiseModulesNoSurfaceBet(String pageId) {
    FeaturedModel model = new FeaturedModel(pageId)
    model.addModule(createInternationalToteModule("Tote Module"))
    Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules = new HashMap<>()
    FanzoneSegmentView fanzoneSegmentView = new FanzoneSegmentView()

    HighlightCarouselModule highlightCarouselModule = createFanzoneHighlightCarouselModule("Highlight Carousel")
    model.addModule(highlightCarouselModule)
    fanzoneSegmentView.getHighlightCarouselModules().put(highlightCarouselModule.getId(), highlightCarouselModule)

    fanzoneSegmentWiseModules.put("Universal", fanzoneSegmentView)
    fanzoneSegmentWiseModules.put("segment-one", fanzoneSegmentView)
    model.setFanzoneSegmentWiseModules(fanzoneSegmentWiseModules)
    model
  }


  FeaturedModel createStructureWithFanzoneSegmentWiseModulesNoMatchingEventName(String pageId) {
    FeaturedModel model = new FeaturedModel(pageId)
    Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules = new HashMap<>()
    FanzoneSegmentView fanzoneSegmentView = new FanzoneSegmentView()

    HighlightCarouselModule highlightCarouselModule = createFanzoneHighlightCarouselModuleNoMatchingTeamExtID("Highlight Carousel")
    model.addModule(highlightCarouselModule)
    fanzoneSegmentView.getHighlightCarouselModules().put(highlightCarouselModule.getId(), highlightCarouselModule)

    fanzoneSegmentWiseModules.put("Universal", fanzoneSegmentView)
    fanzoneSegmentWiseModules.put("segment-one", fanzoneSegmentView)
    model.setFanzoneSegmentWiseModules(fanzoneSegmentWiseModules)
    model
  }

  FeaturedModel createNoStructureWithNoFanzoneSegmentWiseModules(String pageId) {
    FeaturedModel model = new FeaturedModel(pageId)
    model
  }

  InternationalToteRaceModule createInternationalToteModule(String id) {
    InternationalToteRaceModule module = new InternationalToteRaceModule()
    module.setType("InternationalToteRaceModule")
    module.setId(id)
    module.setDisplayOrder(1)
    module
  }

  SurfaceBetModule createSurfaceBetModule(String id) {
    SurfaceBetModule module = new SurfaceBetModule()
    module.setType("SurfaceBetModule")
    module.setId(id)
    module.setDisplayOrder(1)
    SurfaceBetModuleData surfaceBetModuleData =  new SurfaceBetModuleData()
    List<SurfaceBetModuleData> data = new ArrayList()
    data.add(surfaceBetModuleData)
    module.setData(data);
    module
  }

  SurfaceBetModule createFanzoneSurfaceBetModule(String id) {
    SurfaceBetModule module = new SurfaceBetModule()
    module.setType("SurfaceBetModule")
    module.setId(id)
    module.setDisplayOrder(1)
    SurfaceBetModuleData surfaceBetModuleData =  new SurfaceBetModuleData()
    List<SurfaceBetModuleData> data = new ArrayList()
    data.add(surfaceBetModuleData)
    module.setData(data);
    module
  }

  private PopularBetModule createPopularBetModule() {
    PopularBetModule module = new PopularBetModule()
    module.setId("88")
    module.setTitle("popularbets module")
    module.setData(createPopularBetModuleData())
    module.setDisplayOrder(1)
    return module
  }

  private List<PopularBetModuleData> createPopularBetModuleData() {
    List<PopularBetModuleData> moduleData = new ArrayList<>()

    PopularBetModuleData item = new PopularBetModuleData()
    item.setId("432267")
    item.setCategoryId("16")
    item.setName("Fullham vs Chadvick")
    List<OutputMarket> markets = new ArrayList<>()
    OutputMarket market = new OutputMarket()
    market.setId("5543463333")
    market.setName("market_name")
    markets.add(market)
    item.setMarkets(markets)
    item.setPrimaryMarkets(markets)

    moduleData.add(item)

    return moduleData
  }

  TeamBetsModule createTeamBetsModule(String id) {
    TeamBetsModule module = new TeamBetsModule()
    module.setType("TeamBetsModule")
    module.setId(id)
    module.setDisplayOrder(1)
    TeamBetsConfig configdata =  new TeamBetsConfig()
    configdata.setId("tid")
    configdata.setNoOfMaxSelections(4)
    configdata.setFanzoneSegments(Arrays.asList("seg1,seg2"))
    List<TeamBetsConfig> data = new ArrayList()
    data.add(configdata)
    module.setData(data)
    module
  }

  FanBetsModule createFanBetsModule(String id) {
    FanBetsModule module = new FanBetsModule()
    module.setType("FanBetsModule")
    module.setId(id)
    module.setDisplayOrder(1)
    FanBetsConfig configdata =  new FanBetsConfig()
    configdata.setId("tid")
    configdata.setNoOfMaxSelections(4)
    configdata.setFanzoneSegments(Arrays.asList("seg1,seg2"))
    List<FanBetsConfig> data = new ArrayList()
    data.add(configdata)
    module.setData(data)
    module
  }
  HighlightCarouselModule createHighlightCarouselModule(String id) {
    HighlightCarouselModule module = new HighlightCarouselModule()
    module.setType("HighlightCarouselModule")
    module.setId(id)
    SurfaceBetModuleData data = new SurfaceBetModuleData()
    data.setId("123")
    ArrayList list = new ArrayList()
    list.add(data)
    module.setData(list)
    module
  }

  HighlightCarouselModule createFanzoneHighlightCarouselModule(String id) {
    HighlightCarouselModule module = new HighlightCarouselModule()
    module.setType("HighlightCarouselModule")
    module.setId(id)
    EventsModuleData data = new EventsModuleData()
    data.setId("123")
    data.setName("segment-one")
    data.setTeamExtIds("segment-one")
    ArrayList list = new ArrayList()
    list.add(data)
    module.setData(list)
    module
  }

  HighlightCarouselModule createFanzoneHighlightCarouselModuleWithNoTeamExtIds(String id) {
    HighlightCarouselModule module = new HighlightCarouselModule()
    module.setType("HighlightCarouselModule")
    module.setId(id)
    EventsModuleData data = new EventsModuleData()
    data.setId("123")
    data.setName("segment-one")
    data.setTeamExtIds("")
    ArrayList list = new ArrayList()
    list.add(data)
    module.setData(list)
    module
  }

  HighlightCarouselModule createFanzoneHighlightCarouselModuleWithNoTeamExtIds1(String id) {
    HighlightCarouselModule module = new HighlightCarouselModule()
    module.setType("HighlightCarouselModule")
    module.setId(id)
    EventsModuleData data = new EventsModuleData()
    data.setId("123")
    data.setName("segment-xyz")
    data.setTeamExtIds("")
    ArrayList list = new ArrayList()
    list.add(data)
    module.setData(list)
    module
  }

  HighlightCarouselModule createFanzoneHighlightCarouselModuleNoMatchingTeamExtID(String id) {
    HighlightCarouselModule module = new HighlightCarouselModule()
    module.setType("HighlightCarouselModule")
    module.setId(id)
    EventsModuleData data = new EventsModuleData()
    data.setId("123")
    data.setName("segment")
    data.setTeamExtIds("segmentxyz")
    ArrayList list = new ArrayList()
    list.add(data)
    module.setData(list)
    module
  }

  QuickLinkModule createQuickLinkModule(String id) {
    QuickLinkModule qlModule = new QuickLinkModule()
    qlModule.setId("ql")
    qlModule.setTitle("sb")
    qlModule.setDisplayOrder(1)
    qlModule.setType("QuickLinkModule")
    qlModule.setId(id)
    List<QuickLinkData> data = new ArrayList()
    QuickLinkData quickLinkData = new QuickLinkData()
    data.add(quickLinkData)
    qlModule.setData(data);
    qlModule
  }
  EventsModule createFeaturedModule(String id) {
    EventsModuleData eventData = new EventsModuleData();
    eventData.setId("event module");
    eventData.setDisplayOrder(4)
    List<EventsModuleData> data = new ArrayList<>();
    data.add(eventData);

    EventsModule thisModule = new EventsModule();
    thisModule.setId("TEST ID")
    thisModule.setSportId(0)
    thisModule.setTitle("eventmodule")
    thisModule.setData(data)
    thisModule
  }

  InplayModule createInplayModule(String id) {
    InplayModule module = new InplayModule()
    module.setType("InplayModule")
    module.setId(id)
    module.setDisplayOrder(1)
    SportSegment sportSegment =  new SportSegment()
    List<SportSegment> data = new ArrayList()
    data.add(sportSegment)
    module.setData(data);
    module
  }
}
