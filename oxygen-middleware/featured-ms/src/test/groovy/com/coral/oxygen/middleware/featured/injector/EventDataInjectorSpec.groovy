package com.coral.oxygen.middleware.featured.injector

import static com.coral.oxygen.middleware.featured.utils.FeaturedDataUtils.*
import static java.util.stream.Collectors.toMap

import com.coral.oxygen.middleware.common.configuration.GsonConfiguration
import com.coral.oxygen.middleware.common.configuration.MappersConfiguration
import com.coral.oxygen.middleware.common.configuration.SiteServerAPIConfiguration
import com.coral.oxygen.middleware.common.mappers.EventMapper
import com.coral.oxygen.middleware.common.service.DateTimeHelper
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService
import com.coral.oxygen.middleware.common.service.SportsConfig
import com.coral.oxygen.middleware.common.service.featured.IdsCollector
import com.coral.oxygen.middleware.common.utils.OrdinalToNumberConverter
import com.coral.oxygen.middleware.common.utils.QueryFilterBuilder
import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector
import com.coral.oxygen.middleware.featured.utils.DataToOutputData
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContent
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContentItem
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModel
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.*
import java.util.function.Function
import org.joda.time.DateTime
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.beans.factory.annotation.Qualifier
import org.springframework.boot.test.context.SpringBootTest
import spock.lang.Shared
import spock.lang.Specification

@SpringBootTest(classes = [MappersConfiguration.class, SportsConfig.class, GsonConfiguration.class,
  SiteServerAPIConfiguration.class, OrdinalToNumberConverter.class, MarketTemplateNameService.class])
class EventDataInjectorSpec extends Specification {

  EventDataInjector eventDataInjector
  MarketTemplateNameService marketTemplateNameService
  QueryFilterBuilder queryFilterBuilder
  SiteServerApi siteServerApi
  @Autowired
  @Qualifier('featured')
  EventMapper eventMapper

  @Shared
  List<Children> events
  @Shared
  Map<String, Event> eventMap
  @Shared
  IdsCollector idsCollector
  @Shared
  FeaturedModel result

  def setup() {
    siteServerApi = Mock(SiteServerApi)
    marketTemplateNameService = Mock(MarketTemplateNameService)
    def dateTimeHelper = new DateTimeHelper('GMT')
    queryFilterBuilder = new QueryFilterBuilder(marketTemplateNameService)
    eventDataInjector = new EventDataInjector(eventMapper, siteServerApi, queryFilterBuilder, dateTimeHelper,"TwoUpMarket,TWO UP MARKET,TWO UP")
  }

  def setupSpec() {
    ModularContent modularContent = new ModularContent()
    modularContent.addAll(getModularContentItemsFromResource('injector_modular_content.json'))
    ModularContentItem featuredItem = getModularContentItemFromResource('injector_featured_modular_item.json')

    events = getSSEventsFromResource('injector_ss_events_by_eventIds.json')
    eventMap = events.stream()
        .filter({ child -> child.getEvent() != null })
        .map({ child -> child.getEvent() })
        .collect(toMap({ event -> event.getId() }, Function.identity()))
    result = getFeaturedModelFromResource('injector_featured_output_model_result.json')
    idsCollector = new IdsCollector(modularContent, featuredItem)
  }

  def "Verify module data items empty before injections"() {
    def dataItemsStream = result.getModules().stream()
        .map({ module -> module.getData() })
        .flatMap({ collection -> collection.stream() })
        .filter({ item -> item.getOutcomeId() == null })
        .filter({ item -> eventMap.containsKey(String.valueOf(item.getId())) })

    dataItemsStream.forEach({ EventsModuleData item ->
      assert DataToOutputData.verifyDataItemEmpty(item)
    })
    expect:
    true
  }

  def "Verify modules data and nested data after injection"() {
    // action

    siteServerApi.getEventToOutcomeForEvent(*_) >> Optional.of(events) >> Optional.of(new ArrayList<>()) >> Optional.of(new ArrayList<>())
    eventDataInjector.injectData(eventDataInjector.toEventsModuleData(result), idsCollector)

    // results assertions
    result.getModules().stream()
        .map({ outputModule -> outputModule.getData() })
        .filter({ obj -> obj != null })
        .flatMap({ collection -> collection.stream() })
        .filter({ item -> item.getOutcomeId() == null })
        .filter({ item -> eventMap.containsKey(String.valueOf(item.getId())) })
        .forEach({ EventsModuleData item ->
          Event event = eventMap.get(String.valueOf(item.getId()))
          assert DataToOutputData.verifyDataItem(item, event)

          Map<String, Market> eventMarkets = event.getMarkets().stream()
              .filter({ m -> m.getIsActive() && m.getIsAvailable() })
              .collect(toMap({ market -> market.getId() }, Function.identity()))
          assert item.getMarkets().size() == eventMarkets.size()
          item.getMarkets().stream()
              .filter({ m -> eventMarkets.containsKey(m.getId()) })
              .forEach({ m ->
                Market market = eventMarkets.get(m.getId())
                assert DataToOutputData.verifyMarket(m, market)

                Map<String, Outcome> outcomes = market.getOutcomes()
                    .stream()
                    .collect(toMap({ outcome -> outcome.getId() }, Function.identity()))
                m.getOutcomes().stream()
                    .filter({ o -> outcomes.containsKey(o.getId()) })
                    .forEach({ o ->
                      Outcome outcome = outcomes.get(o.getId())
                      assert DataToOutputData.verifyOutcome(o, outcome)

                      Map<String, Price> priceMap =
                          outcome.getPrices().stream()
                          .collect(toMap({ price -> price.getId() }, Function.identity()))
                      o.getPrices().stream()
                          .filter({ p -> priceMap.containsKey(p.getId()) })
                          .forEach({ p ->
                            Price price = priceMap.get(p.getId())
                            assert DataToOutputData.verifyPrice(p, price)
                          })
                    })
              })
        })
    expect:
    true
  }

  def "Verify modules data with Market Data Selection type"() {
    given:
    def marketId = '111'
    def eventId = 1
    idsCollector.setMarketIds(Collections.singletonList(marketId))
    siteServerApi.getWholeEventToOutcomeForMarket(*_) >> createEventForMarket(eventId, marketId)
    siteServerApi.getEventToOutcomeForEvent(*_) >> Optional.of(new ArrayList<>())

    when:
    def data = createEventModuleData(eventId)
    eventDataInjector.injectData(data, idsCollector)

    then:
    data.size() == 1
    def event = data.get(0)
    event.getId() == eventId
    event.getMarkets().size() == 1
    event.getMarkets().get(0).getId() == marketId
    event.getPrimaryMarkets().size() == 1
    event.getPrimaryMarkets().get(0).getId() == marketId
  }

  def "Verify resulted events are excluded when Market Data Selection type"() {
    given:
    def marketId = '111'
    def eventId = 1
    idsCollector.setMarketIds(Collections.singletonList(marketId))
    def resultedEvent = createEventForMarket(eventId, marketId, true)
    siteServerApi.getWholeEventToOutcomeForMarket(*_) >> resultedEvent
    siteServerApi.getEventToOutcomeForEvent(*_) >> Optional.of(new ArrayList<>())

    when:
    def data = createEventModuleData(eventId)
    eventDataInjector.injectData(data, idsCollector)

    then:
    data.size() == 1
    def event = data.get(0)
    event.getId() == eventId
    event.getMarkets().size() == 0
    event.getPrimaryMarkets().size() == 0
  }

  def "Verify events with passed suspendAtTime are excluded when Market Data Selection type"() {
    given:
    def marketId = '111'
    def eventId = 1
    idsCollector.setMarketIds(Collections.singletonList(marketId))
    def resultedEvent = createEventForMarket(eventId, marketId, null, DateTime.now().minusMinutes(1).toString())
    siteServerApi.getWholeEventToOutcomeForMarket(*_) >> resultedEvent
    siteServerApi.getEventToOutcomeForEvent(*_) >> Optional.of(new ArrayList<>())

    when:
    def data = createEventModuleData(eventId)
    eventDataInjector.injectData(data, idsCollector)

    then:
    data.size() == 1
    def event = data.get(0)
    event.getId() == eventId
    event.getMarkets().size() == 0
    event.getPrimaryMarkets().size() == 0
  }

  List<EventsModuleData> createEventModuleData(long eventId) {
    EventsModuleData eventsModuleData = new EventsModuleData()
    eventsModuleData.setId(eventId)
    Collections.singletonList(eventsModuleData)
  }

  Optional<List<Event>> createEventForMarket(long eventId, String marketId, Boolean isResulted=null, String suspendTime = null) {
    Event event = new Event()
    event.id = String.valueOf(eventId)
    event.isActive = Boolean.TRUE
    event.isResulted = isResulted
    event.suspendAtTime = suspendTime
    def market = new Market()
    market.id = marketId
    market.isActive = Boolean.TRUE
    def children = new Children()
    children.market = market
    event.children = Collections.singletonList(children)
    Optional.of(Collections.singletonList(event))
  }

  def "Verify events with passed suspendAtTime are excluded when Market Data Selection type1"() {
    given:
    def marketId = '111'
    def eventId = 1
    idsCollector.setMarketIds(Collections.singletonList(marketId))
    def resultedEvent = createEventForMarket1(eventId, marketId, null, DateTime.now().plusMinutes(1).toString())
    siteServerApi.getWholeEventToOutcomeForMarket(*_) >> resultedEvent
    siteServerApi.getEventToOutcomeForEvent(*_) >> Optional.of(new ArrayList<>())

    when:
    def data = createEventModuleData1(eventId)
    eventDataInjector.injectData(data, idsCollector)

    then:
    data.size() == 1
    def event = data.get(0)
    event.getId() == eventId
    event.getMarkets().size() == 1
  }

  List<EventsModuleData> createEventModuleData1(long eventId) {
    EventsModuleData eventsModuleData = new EventsModuleData()
    eventsModuleData.setId(eventId)
    Collections.singletonList(eventsModuleData)
  }

  Optional<List<Event>> createEventForMarket1(long eventId, String marketId, Boolean isResulted=null, String suspendTime = null) {
    Event event = new Event()
    event.id = String.valueOf(eventId)
    event.isActive = Boolean.TRUE
    event.isResulted = isResulted
    event.suspendAtTime = suspendTime
    event.isStarted = Boolean.TRUE
    def market = new Market()
    market.id = marketId
    market.isActive = Boolean.TRUE
    def children = new Children()
    children.market = market
    event.children = Collections.singletonList(children)
    Optional.of(Collections.singletonList(event))
  }

  def "Verify events with passed suspendAtTime are excluded when Market Data Selection type2"() {
    given:
    def marketId = '111'
    def eventId = 1
    idsCollector.setMarketIds(Collections.singletonList(marketId))
    def resultedEvent = createEventForMarket2(eventId, marketId, null, DateTime.now().plusMinutes(1).toString())
    siteServerApi.getWholeEventToOutcomeForMarket(*_) >> resultedEvent
    siteServerApi.getEventToOutcomeForEvent(*_) >> Optional.of(new ArrayList<>())

    when:
    def data = createEventModuleData2(eventId)
    eventDataInjector.injectData(data, idsCollector)

    then:
    data.size() == 1
    def event = data.get(0)
    event.getId() == eventId
    event.getMarkets().size() == 1
  }
  def "Verify modules data with Market Data With 2 up"() {
    given:
    def eventId = 123l
    idsCollector.setEventsIds(Collections.singletonList(eventId))
    idsCollector.setMarketIds(null)
    siteServerApi.getEventToOutcomeForEvent(*_) >> Optional.of(getChildrens())

    when:
    def data = createEventModuleData(eventId)
    eventDataInjector.injectData(data, idsCollector,"2UpMarket")

    then:
    data.size() == 1
    def event = data.get(0)
    event.getId() == eventId

  }
  List<EventsModuleData> createEventModuleData2(long eventId) {
    EventsModuleData eventsModuleData = new EventsModuleData()
    eventsModuleData.setId(eventId)
    Collections.singletonList(eventsModuleData)
  }

  Optional<List<Event>> createEventForMarket2(long eventId, String marketId, Boolean isResulted=null, String suspendTime = null) {
    Event event = new Event()
    event.id = String.valueOf(eventId)
    event.isActive = Boolean.TRUE
    event.isResulted = isResulted
    event.suspendAtTime = suspendTime
    def market = new Market()
    market.id = marketId
    market.isActive = Boolean.TRUE
    def children = new Children()
    children.market = market
    event.children = Collections.singletonList(children)
    Optional.of(Collections.singletonList(event))
  }


  private static List<Children> getChildrens(){

    List<Children> result=new ArrayList<>();
    Children eventCh=new Children();
    List<Children> marketsCh=createMarketChilren();
    Event event=new Event();
    event.setId("124");
    event.isActive = Boolean.TRUE
    event.setChildren(marketsCh);
    eventCh.setEvent(event);
    result.add(eventCh);
    return result;
  }
  private static List<Children> createMarketChilren() {
    List<Children> markets=new ArrayList<>();
    markets.add(getChildrenWithMarket("Match result","121"));
    markets.add(getChildrenWithMarket("TWO UP","1213"));
    return markets;
  }

  private static Children getChildrenWithMarket(String marketName,String id) {
    Children mar= new Children();
    mar.setMarket(createMarket(marketName,id));
    return mar;
  }

  private static Market createMarket(String name,String id) {
    Market mr=new Market();
    mr.setName(name);
    mr.id = id
    mr.isActive = Boolean.TRUE
    return mr;
  }

}
