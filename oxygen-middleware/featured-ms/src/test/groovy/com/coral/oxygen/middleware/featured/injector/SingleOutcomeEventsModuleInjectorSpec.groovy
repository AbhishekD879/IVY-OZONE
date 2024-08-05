package com.coral.oxygen.middleware.featured.injector

import com.coral.oxygen.middleware.common.configuration.GsonConfiguration
import com.coral.oxygen.middleware.common.configuration.MappersConfiguration
import com.coral.oxygen.middleware.common.configuration.SiteServerAPIConfiguration
import com.coral.oxygen.middleware.common.mappers.EventMapper
import com.coral.oxygen.middleware.common.service.DateTimeHelper
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService
import com.coral.oxygen.middleware.common.service.SportsConfig
import com.coral.oxygen.middleware.common.service.featured.IdsCollector
import com.coral.oxygen.middleware.common.utils.OrdinalToNumberConverter
import com.coral.oxygen.middleware.featured.service.injector.SingleOutcomeEventsModuleInjector
import com.coral.oxygen.middleware.featured.utils.DataToOutputData
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContent
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContentItem
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome
import com.coral.oxygen.middleware.pojos.model.output.OutputPrice
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModel
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.*
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.beans.factory.annotation.Qualifier
import org.springframework.boot.test.context.SpringBootTest
import spock.lang.Specification

import java.security.SecureRandom
import java.util.function.Function
import java.util.stream.Collectors

import static com.coral.oxygen.middleware.featured.utils.FeaturedDataUtils.*
import static java.util.function.Function.identity
import static java.util.stream.Collectors.toMap

@SpringBootTest(classes = [
  MappersConfiguration.class, SportsConfig.class, GsonConfiguration.class,
  SiteServerAPIConfiguration.class, OrdinalToNumberConverter.class, MarketTemplateNameService.class
])
class SingleOutcomeEventsModuleInjectorSpec extends Specification {
  SingleOutcomeEventsModuleInjector singleOutcomeDataInjector
  SiteServerApi siteServerApi
  @Autowired
  @Qualifier("featured")
  EventMapper eventMapper

  def setup() {
    siteServerApi = Mock(SiteServerApi)
    singleOutcomeDataInjector = new SingleOutcomeEventsModuleInjector(eventMapper, siteServerApi)
  }

  def "Inject Data using Model"() {

    given:
    FeaturedModel featuredModel = getFeaturedModelFromResource("injector_featured_output_model_result.json")
    List<ModularContentItem> items = getModularContentItemsFromResource("injector_modular_content.json")
    ModularContent modularContent = new ModularContent()
    modularContent.addAll(items)
    ModularContentItem featuredContentItem = getModularContentItemFromResource("injector_featured_modular_item.json")
    IdsCollector idsCollector = new IdsCollector(modularContent, featuredContentItem)
    List<Event> events = getSSEventToOutcomeForOutcome("injector_single_outcome_ids.json")

    Map<String, Event> eventMap = events.stream()
        .collect(toMap({ event -> event.getId() }, identity()))

    featuredModel.getModules().stream()
        .filter({ object -> object != null })
        .map({ outputModule -> outputModule.getData() })
        .flatMap({ collection -> collection.stream() })
        .filter({ item -> item.getOutcomeId() != null })
        .filter({ item -> eventMap.containsKey(String.valueOf(item.getId())) })
        .forEach({ item ->
          assert DataToOutputData.verifyDataItemEmpty(item)
        })

    when:
    this.siteServerApi.getEventToOutcomeForOutcome(_ as List, _, _) >> Optional.of(events)
    singleOutcomeDataInjector.injectData(singleOutcomeDataInjector.toEventsModuleData(featuredModel), idsCollector)


    then:
    featuredModel.getModules().stream()
        .filter({ object -> object != null })
        .map({ outputModule -> outputModule.getData() })
        .flatMap({ collection -> collection.stream() })
        .filter({ item -> item.getOutcomeId() != null })
        .filter({ item -> eventMap.containsKey(String.valueOf(item.getId())) })
        .forEach({ item ->
          Event event = eventMap.get(String.valueOf(item.getId()))
          DataToOutputData.verifyDataItem(item, event)


          Map<String, Market> eventMarkets = event.getMarkets().stream()
              .filter({ m -> m.getIsActive() && m.getIsAvailable() })
              .collect(toMap({ market -> market.getId() }, Function.identity()))

          item.getMarkets().size() == 1
          item.getMarkets().stream()
              .filter({ m -> eventMarkets.containsKey(m.getId()) })
              .forEach({ m ->
                Market market = eventMarkets.get(m.getId())

                DataToOutputData.verifyMarket(m, market)

                // Verify outcomes
                Map<String, Outcome> outcomes =
                    market.getOutcomes().stream()
                    .collect(toMap({ outcome -> outcome.getId() }, Function.identity()))
                m.getOutcomes().stream()
                    .filter({ o -> outcomes.containsKey(o.getId()) })
                    .forEach({ o ->
                      Outcome outcome = outcomes.get(o.getId())

                      verifyOutcome(o, outcome)

                      // Verify prices
                      Map<String, Price> priceMap = outcome.getPrices().stream()
                          .collect(toMap({ price -> price.getId() }, Function.identity()))
                      o.getPrices().stream()
                          .filter({ p -> priceMap.containsKey(p.getId()) })
                          .forEach({ p ->
                            Price price = priceMap.get(p.getId())

                            verifyPrice(p, price)
                          })
                    })
              })
        })
  }

  def "Inject Data using Model Fanzone"() {

    given:
    FeaturedModel featuredModel = getFeaturedModelFromResource("injector_featured_output_model_result.json")
    List<ModularContentItem> items = getModularContentItemsFromResource("injector_modular_content.json")
    ModularContent modularContent = new ModularContent()
    modularContent.addAll(items)
    ModularContentItem featuredContentItem = getModularContentItemFromResource("injector_featured_modular_item.json")
    IdsCollector idsCollector = new IdsCollector(modularContent, featuredContentItem)
    List<Event> events = getSSEventToOutcomeForOutcome("injector_single_outcome_ids.json")

    Map<String, Event> eventMap = events.stream()
        .collect(toMap({ event -> event.getId() }, identity()))

    featuredModel.getModules().stream()
        .filter({ object -> object != null })
        .map({ outputModule -> outputModule.getData() })
        .flatMap({ collection -> collection.stream() })
        .filter({ item -> item.getOutcomeId() != null })
        .filter({ item -> eventMap.containsKey(String.valueOf(item.getId())) })
        .forEach({ item ->
          assert DataToOutputData.verifyDataItemEmpty(item)
        })

    when:
    this.siteServerApi.getEventToOutcomeForOutcome(_ as List, _, _, _) >> Optional.of(events)
    singleOutcomeDataInjector.injectData(singleOutcomeDataInjector.toEventsModuleData(featuredModel), idsCollector, true)


    then:
    featuredModel.getModules().stream()
        .filter({ object -> object != null })
        .map({ outputModule -> outputModule.getData() })
        .flatMap({ collection -> collection.stream() })
        .filter({ item -> item.getOutcomeId() != null })
        .filter({ item -> eventMap.containsKey(String.valueOf(item.getId())) })
        .forEach({ item ->
          Event event = eventMap.get(String.valueOf(item.getId()))
          DataToOutputData.verifyDataItem(item, event)


          Map<String, Market> eventMarkets = event.getMarkets().stream()
              .filter({ m -> m.getIsActive() && m.getIsAvailable() })
              .collect(toMap({ market -> market.getId() }, Function.identity()))

          item.getMarkets().size() == 1
          item.getMarkets().stream()
              .filter({ m -> eventMarkets.containsKey(m.getId()) })
              .forEach({ m ->
                Market market = eventMarkets.get(m.getId())

                DataToOutputData.verifyMarket(m, market)

                // Verify outcomes
                Map<String, Outcome> outcomes =
                    market.getOutcomes().stream()
                    .collect(toMap({ outcome -> outcome.getId() }, Function.identity()))
                m.getOutcomes().stream()
                    .filter({ o -> outcomes.containsKey(o.getId()) })
                    .forEach({ o ->
                      Outcome outcome = outcomes.get(o.getId())

                      verifyOutcome(o, outcome)

                      // Verify prices
                      Map<String, Price> priceMap = outcome.getPrices().stream()
                          .collect(toMap({ price -> price.getId() }, Function.identity()))
                      o.getPrices().stream()
                          .filter({ p -> priceMap.containsKey(p.getId()) })
                          .forEach({ p ->
                            Price price = priceMap.get(p.getId())

                            verifyPrice(p, price)
                          })
                    })
              })
        })
  }

  def "Inject Data using Model Fanzone IfCondition"() {

    given:
    FeaturedModel featuredModel = getFeaturedModelFromResource("injector_featured_output_model_result.json")
    List<ModularContentItem> items = getModularContentItemsFromResource("injector_modular_content.json")
    ModularContent modularContent = new ModularContent()
    modularContent.addAll(items)
    ModularContentItem featuredContentItem = getModularContentItemFromResource("injector_featured_modular_item.json")
    IdsCollector idsCollector = new IdsCollector(modularContent, featuredContentItem)
    List<Event> events = getSSEventToOutcomeForOutcome("injector_single_outcome_ids.json")

    Map<String, Event> eventMap = events.stream()
        .collect(toMap({ event -> event.getId() }, identity()))

    when:
    this.siteServerApi.getEventToOutcomeForOutcome(_ as List, _, _, _) >> Optional.empty()
    singleOutcomeDataInjector.injectData(singleOutcomeDataInjector.toEventsModuleData(featuredModel), idsCollector, true)


    then:
    assert events != null
  }

  def "Inject Data using ModuleDataItems"() {

    given:
    FeaturedModel featuredModel = getFeaturedModelFromResource("injector_featured_output_model_result.json")
    List<ModularContentItem> items = getModularContentItemsFromResource("injector_modular_content.json")
    ModularContent modularContent = new ModularContent()
    modularContent.addAll(items)
    ModularContentItem featuredContentItem = getModularContentItemFromResource("injector_featured_modular_item.json")
    IdsCollector idsCollector = new IdsCollector(modularContent, featuredContentItem)
    List<Event> events = getSSEventToOutcomeForOutcome("injector_single_outcome_ids.json")

    Map<String, Event> eventMap = events.stream()
        .collect(toMap({ event -> event.getId() }, identity()))

    featuredModel.getModules().stream()
        .filter({ object -> object != null })
        .map({ outputModule -> outputModule.getData() })
        .flatMap({ collection -> collection.stream() })
        .filter({ item -> item.getOutcomeId() != null })
        .filter({ item -> eventMap.containsKey(String.valueOf(item.getId())) })
        .forEach({ item ->
          assert DataToOutputData.verifyDataItemEmpty(item)
        })

    List<EventsModuleData> moduleDataItems = featuredModel.getModules().get(0).getData()

    when:
    this.siteServerApi.getEventToOutcomeForOutcome(_ as List, _, _) >> Optional.of(events)
    singleOutcomeDataInjector.injectData(moduleDataItems, idsCollector)


    then:
    EventsModuleData item = featuredModel.getModules().stream()
        .filter({ object -> object != null })
        .map({ outputModule -> outputModule.getData() })
        .flatMap({ collection -> collection.stream() })
        .filter({ item -> item.getOutcomeId() != null })
        .filter({ item -> eventMap.containsKey(String.valueOf(item.getId())) })
        .findFirst().get()

    Event event = eventMap.get(String.valueOf(item.getId()))
    DataToOutputData.verifyDataItem(item, event)


    Map<String, Market> eventMarkets = event.getMarkets().stream()
        .filter({ m -> m.getIsActive() && m.getIsAvailable() })
        .collect(toMap({ market -> market.getId() }, Function.identity()))

    item.getMarkets().size() == 1
    item.getMarkets().stream()
        .filter({ m -> eventMarkets.containsKey(m.getId()) })
        .forEach({ m ->
          Market market = eventMarkets.get(m.getId())

          DataToOutputData.verifyMarket(m, market)

          // Verify outcomes
          Map<String, Outcome> outcomes =
              market.getOutcomes().stream()
              .collect(toMap({ outcome -> outcome.getId() }, Function.identity()))
          m.getOutcomes().stream()
              .filter({ o -> outcomes.containsKey(o.getId()) })
              .forEach({ o ->
                Outcome outcome = outcomes.get(o.getId())

                verifyOutcome(o, outcome)

                // Verify prices
                Map<String, Price> priceMap = outcome.getPrices().stream()
                    .collect(toMap({ price -> price.getId() }, Function.identity()))
                o.getPrices().stream()
                    .filter({ p -> priceMap.containsKey(p.getId()) })
                    .forEach({ p ->
                      Price price = priceMap.get(p.getId())

                      verifyPrice(p, price)
                    })
              })
        })
  }

  def "Check real eventName is set as name to EventModuleData"() {
    given:
    List<EventsModuleData> eventData = createEventData()

    def outcomeName = "Outcome name"
    def eventName = "Event name"

    and:
    siteServerApi.getEventToOutcomeForOutcome(*_) >> createEvents(eventData, eventName, outcomeName)

    when:
    singleOutcomeDataInjector.injectData(eventData, new IdsCollector(Collections.singletonList(12344L)))

    then:
    !eventData.isEmpty()
    eventData.stream().allMatch({e -> e.getName().equals(eventName)})
  }

  Optional<List<Event>> createEvents(List<EventsModuleData> eventsModuleData, String eventName, String outcomeName) {
    def random  = new SecureRandom();
    return Optional.of(eventsModuleData.stream().map({d ->
      def outcome = new Outcome()
      outcome.id = d.getOutcomeId()
      outcome.name = outcomeName
      def outcomeChild = new Children()
      outcomeChild.outcome = outcome

      def market = new Market()
      market.id = random.nextInt(10000)
      market.children = Collections.singletonList(outcomeChild)
      def marketChild = new Children()
      marketChild.market = market

      def event = new Event()
      event.id = String.valueOf(random.nextInt(10000))
      event.name = eventName
      event.children = Collections.singletonList(marketChild)
      return event
    }).collect(Collectors.toList()))
  }

  List<EventsModuleData> createEventData() {
    def event1 = new EventsModuleData()
    event1.setOutcomeId(12345)
    def event2 = new EventsModuleData()
    event2.setOutcomeId(4566788)
    Arrays.asList(event1, event2)
  }

  def verifyPrice(OutputPrice p, Price price) {
    assert p.getPriceType() == price.getPriceType()
    assert p.getPriceNum() == price.getPriceNum()
    assert p.getPriceDec() == price.getPriceDec()
    assert p.getPriceDen() == price.getPriceDen()
    assert p.getHandicapValueDec() == price.getHandicapValueDec().replace(",", "")
    assert p.getRawHandicapValue() == price.getRawHandicapValue()

    return true
  }

  def verifyOutcome(OutputOutcome o, Outcome outcome) {
    assert o.getName() != outcome.getName()
    assert o.getOutcomeMeaningMajorCode() == outcome.getOutcomeMeaningMajorCode()
    assert o.getOutcomeMeaningMinorCode() == outcome.getOutcomeMeaningMinorCode()
    assert o.getOutcomeMeaningScores() == outcome.getOutcomeMeaningScores()
    assert o.getRunnerNumber() == outcome.getRunnerNumber()
    assert o.getResulted() == outcome.getIsResulted()
    assert o.getOutcomeStatusCode() == outcome.getOutcomeStatusCode()
    assert o.getLiveServChannels() == outcome.getLiveServChannels()
    assert (o.getCorrectPriceType() == null || o.getCorrectPriceType() == "SP" || o.getCorrectPriceType() == "LP")
    assert Arrays.asList(null, 1, 2, 3).contains(o.getCorrectedOutcomeMeaningMinorCode())

    return true
  }
}
