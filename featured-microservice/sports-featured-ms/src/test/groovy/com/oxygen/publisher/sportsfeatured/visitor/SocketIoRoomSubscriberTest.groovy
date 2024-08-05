package com.oxygen.publisher.sportsfeatured.visitor

import com.corundumstudio.socketio.SocketIOClient
import com.oxygen.publisher.sportsfeatured.context.SportsSessionContext
import com.oxygen.publisher.sportsfeatured.model.module.*
import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData
import com.oxygen.publisher.sportsfeatured.model.module.data.PopularAccaModuleData
import com.oxygen.publisher.sportsfeatured.model.module.data.PopularBetModuleData
import com.oxygen.publisher.sportsfeatured.model.module.data.TrendingPosition
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.SportSegment
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.TypeSegment
import spock.lang.Specification

class SocketIoRoomSubscriberTest extends Specification {
  private SocketIOClient socketIoClient
  private FeaturedModuleVisitor visitor

  void setup() {
    socketIoClient = Mock(SocketIOClient)
    visitor = new SocketIoRoomSubscriber(socketIoClient, Mock(SportsSessionContext))
  }

  def "Inplay module subscription"() {
    given:
    AbstractFeaturedModule inplayModule = new InplayModule()
    inplayModule.showExpanded = true
    inplayModule.id = "abc-123"
    inplayModule.sportId = 0
    def sportSegment = new SportSegment()
    def typeSegment = new TypeSegment()
    typeSegment.events = [
      eventData("123"),
      eventData("321")
    ]
    def typeSegment2 = new TypeSegment()
    typeSegment2.events = [eventData("456")]
    sportSegment.eventsByTypeName = [typeSegment, typeSegment2]
    inplayModule.data = [sportSegment]
    when:
    visitor.visit(inplayModule)
    then:
    1 * socketIoClient.joinRoom("0#abc-123")
    1 * socketIoClient.joinRoom("123")
    1 * socketIoClient.joinRoom("321")
    1 * socketIoClient.joinRoom("456")
  }

  def "Inplay module with segment subscription"() {
    given:
    AbstractFeaturedModule inplayModule = new InplayModule()
    inplayModule.showExpanded = true
    inplayModule.id = "abc-123"
    inplayModule.sportId = 0
    def sportSegment = new SportSegment()
    def typeSegment = new TypeSegment()
    typeSegment.events = [
      eventData("123"),
      eventData("321")
    ]
    def typeSegment2 = new TypeSegment()
    typeSegment2.events = [eventData("456")]
    sportSegment.eventsByTypeName = [typeSegment, typeSegment2]
    inplayModule.data = [sportSegment]
    when:
    visitor.visit(inplayModule,"segment")
    then:
    1 * socketIoClient.joinRoom("0#segment#abc-123")
    1 * socketIoClient.joinRoom("123")
    1 * socketIoClient.joinRoom("321")
    1 * socketIoClient.joinRoom("456")
  }
  def "Inplay module with segment subscription expanded false"() {
    given:
    AbstractFeaturedModule inplayModule = new InplayModule()
    inplayModule.showExpanded = false
    inplayModule.id = "abc-123"
    inplayModule.sportId = 0
    def sportSegment = new SportSegment()
    def typeSegment = new TypeSegment()
    typeSegment.events = [
      eventData("123"),
      eventData("321")
    ]
    def typeSegment2 = new TypeSegment()
    typeSegment2.events = [eventData("456")]
    sportSegment.eventsByTypeName = [typeSegment, typeSegment2]
    inplayModule.data = [sportSegment]
    when:
    visitor.visit(inplayModule,"segment")
    then:
    0 * socketIoClient.joinRoom("0#segment#abc-123")
    0 * socketIoClient.joinRoom("123")
    0 * socketIoClient.joinRoom("321")
    0 * socketIoClient.joinRoom("456")
  }

  def "If Inplay module is not expanded then no subscription happens"() {
    given:
    AbstractFeaturedModule inplayModule = new InplayModule()
    inplayModule.id = "abc"
    inplayModule.showExpanded = false
    when:
    visitor.visit(inplayModule)
    then:
    0 * socketIoClient.joinRoom(_)
  }

  def "If Events module is not expanded then no subscription happens"() {
    given:
    AbstractFeaturedModule eventsModule = new EventsModule()
    eventsModule.id = "abc"
    eventsModule.showExpanded = false
    when:
    visitor.visit(eventsModule)
    then:
    0 * socketIoClient.joinRoom(_)
  }

  def "Events Modules subscription"() {
    given:
    EventsModule eventsModule = new EventsModule()
    eventsModule.id = "abc"
    eventsModule.showExpanded = true
    def eventsModuleData = new EventsModuleData()
    eventsModuleData.id = "123"
    def eventsModuleData2 = new EventsModuleData()
    eventsModuleData2.id = "312"
    eventsModule.data = [
      eventsModuleData,
      eventsModuleData2
    ]
    when:
    visitor.visit(eventsModule)
    then:
    0 * socketIoClient.joinRoom("abc")
    1 * socketIoClient.joinRoom("123")
    1 * socketIoClient.joinRoom("312")
  }

  def "QuickLink module subcription on module id"() {
    given:
    QuickLinkModule quickLinkModule = new QuickLinkModule()
    quickLinkModule.id = "abc"
    quickLinkModule.sportId = 0
    when:
    visitor.visit(quickLinkModule)
    then:
    1 * socketIoClient.joinRoom("0#abc")
  }

  def "Surfacebet module subscription"() {
    given:
    def surfaceBetModule = new SurfaceBetModule()
    surfaceBetModule.id = "abc"
    surfaceBetModule.sportId = 0
    surfaceBetModule.showExpanded = true
    when:
    visitor.visit(surfaceBetModule)
    then:
    1 * socketIoClient.joinRoom("0#abc")
  }

  def "AEM carousel module subscription"() {
    given:
    def aemCarouselModule = new AemBannersModule()
    aemCarouselModule.id = "abc"
    aemCarouselModule.sportId = 0
    aemCarouselModule.showExpanded = true
    when:
    visitor.visit(aemCarouselModule)
    then:
    1 * socketIoClient.joinRoom("0#abc")
  }

  def "Highlightcarousel module subscription"() {
    given:
    def highlightCarouselModule = new HighlightCarouselModule()
    highlightCarouselModule.id = "abc"
    highlightCarouselModule.showExpanded = true
    when:
    visitor.visit(highlightCarouselModule)
    then:
    0 * socketIoClient.joinRoom("abc")
  }

  def "RacingModule module subscription on module id"() {
    given:
    RacingModule racingModule = new RacingModule()
    racingModule.id = "abc"
    racingModule.sportId = 0
    when:
    visitor.visit(racingModule)
    then:
    1 * socketIoClient.joinRoom("0#abc")
  }

  def "RacingEventsModule module subscription on module id"() {
    given:
    RacingEventsModule  racingEventsModule = new RacingEventsModule()
    racingEventsModule.id = "abc"
    racingEventsModule.sportId = 0
    when:
    visitor.visit(racingEventsModule)
    then:
    1 * socketIoClient.joinRoom("0#abc")
  }

  def "VirtualRaceModule module subscription on module id"() {
    given:
    VirtualRaceModule  virtualRaceModule = new VirtualRaceModule ()
    virtualRaceModule.id = "abc"
    virtualRaceModule.sportId = 0
    when:
    visitor.visit(virtualRaceModule)
    then:
    1 * socketIoClient.joinRoom("0#abc")
  }

  def "BybWidget module subscription"() {
    given:
    def bybWidgetModule = new BybWidgetModule()
    bybWidgetModule.id = "abc"
    bybWidgetModule.sportId = 0
    bybWidgetModule.showExpanded = true
    when:
    visitor.visit(bybWidgetModule)
    then:
    1 * socketIoClient.joinRoom("0#abc")
  }

  def "Lucky Dip module subscription"() {
    given:
    LuckyDipModule luckyDipModule = new LuckyDipModule()
    luckyDipModule.id = "abc"
    luckyDipModule.sportId = 0
    luckyDipModule.showExpanded = true
    when:
    visitor.visit(luckyDipModule)
    then:
    1 * socketIoClient.joinRoom("0#abc")
  }

  def "Popular Acca module subscription"() {
    given:
    PopularAccaModule popularAccaModule = new PopularAccaModule()
    popularAccaModule.id = "abc"
    popularAccaModule.sportId = 0
    popularAccaModule.showExpanded = true

    PopularAccaModuleData data = new PopularAccaModuleData();
    TrendingPosition position = new TrendingPosition();
    PopularBetModuleData betData = new PopularBetModuleData();
    betData.setId("123");
    position.setEvent(betData);
    data.setPositions(Arrays.asList(position));

    popularAccaModule.setData(Arrays.asList(data));
    when:
    visitor.visit(popularAccaModule)
    then:
    1 * socketIoClient.joinRoom("0#abc")
  }

  def "super button  module subscription"() {
    given:
    SuperButtonModule superModule = new SuperButtonModule()
    superModule.id = "abc"
    superModule.sportId = 0
    superModule.showExpanded = true
    when:
    visitor.visit(superModule)
    then:
    1 * socketIoClient.joinRoom("0#abc")
  }

  private EventsModuleData eventData(String eventId) {
    EventsModuleData eventsModuleData = new EventsModuleData()
    eventsModuleData.id = eventId
    return eventsModuleData
  }
}
