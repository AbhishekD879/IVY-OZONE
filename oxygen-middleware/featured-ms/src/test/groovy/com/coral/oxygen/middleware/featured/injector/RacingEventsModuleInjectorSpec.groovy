package com.coral.oxygen.middleware.featured.injector

import com.coral.oxygen.middleware.common.configuration.GsonConfiguration
import com.coral.oxygen.middleware.common.configuration.MappersConfiguration
import com.coral.oxygen.middleware.common.configuration.SiteServerAPIConfiguration
import com.coral.oxygen.middleware.common.mappers.EventMapper
import com.coral.oxygen.middleware.common.mappers.RacingForOutcomeMapper
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService
import com.coral.oxygen.middleware.common.service.SportsConfig
import com.coral.oxygen.middleware.common.service.featured.IdsCollector
import com.coral.oxygen.middleware.common.utils.OrdinalToNumberConverter
import com.coral.oxygen.middleware.featured.service.injector.ConsumeBirHREvents
import com.coral.oxygen.middleware.featured.service.injector.RacingEventsModuleInjector
import com.coral.oxygen.middleware.featured.utils.DataToOutputData
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContent
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContentItem
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModel
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.*
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.beans.factory.annotation.Qualifier
import org.springframework.boot.test.context.SpringBootTest
import spock.lang.Ignore
import spock.lang.Shared
import spock.lang.Specification

import static com.coral.oxygen.middleware.featured.utils.FeaturedDataUtils.*
import static java.lang.String.valueOf
import static java.util.function.Function.identity
import static java.util.stream.Collectors.toMap

@SpringBootTest(classes = [
  MappersConfiguration.class, SportsConfig.class, GsonConfiguration.class,
  SiteServerAPIConfiguration.class, OrdinalToNumberConverter.class, MarketTemplateNameService.class
])
class RacingEventsModuleInjectorSpec extends Specification {
  RacingEventsModuleInjector racingDataInjector
  ConsumeBirHREvents consumeBirHREvents
  MarketTemplateNameService marketTemplateNameService
  SiteServerApi siteServerAPI
  @Autowired
  @Qualifier("featured")
  EventMapper eventMapper
  @Autowired
  RacingForOutcomeMapper racingForOutcomeMapper

  @Shared
  IdsCollector idsCollector
  @Shared
  FeaturedModel model
  @Shared
  List<Children> events
  @Shared
  Map<String, Event> eventMap

  def setup() {
    consumeBirHREvents = Mock(ConsumeBirHREvents)
    siteServerAPI = Mock(SiteServerApi)
    marketTemplateNameService = Mock(MarketTemplateNameService)
    racingDataInjector = new RacingEventsModuleInjector(eventMapper, siteServerAPI
        ,
        racingForOutcomeMapper,
        marketTemplateNameService,
        new com.coral.oxygen.middleware.common.mappers.SimpleRacingFormEventMapper(), consumeBirHREvents)
  }

  def setupSpec() {
    ModularContent modularContent = new ModularContent()
    modularContent.addAll(getModularContentItemsFromResource("injector_modular_content.json"))
    ModularContentItem featuredItem = getModularContentItemFromResource("injector_featured_modular_item.json")

    events = getSSEventsFromResource("injector_horse_racing_ids.json")
    eventMap = events.stream()
        .filter({ child -> child.getEvent() != null })
        .map({ child -> child.getEvent() })
        .collect(toMap({ event -> event.getId() }, identity()))
    model = getFeaturedModelFromResource("injector_featured_output_model_result.json")
    idsCollector = new IdsCollector(modularContent, featuredItem)
  }

  def "Verify module data items empty before injections"() {
    def dataItemsStream = model.getModules().stream()
        .map({ outputModule -> outputModule.getData() })
        .filter({ item -> item != null })
        .flatMap({ collection -> collection.stream() })
        .filter({ item -> item.getId() != null })
        .filter({ item -> item.getOutcomeId() == null })
        .filter({ item -> eventMap.containsKey(valueOf(item.getId())) })

    dataItemsStream.forEach({ item ->
      assert DataToOutputData.verifyDataItemEmpty(item)
    })
    expect:
    true
  }

  def "Verify modules data and nested data after injection"() {
    this.siteServerAPI.getEventToOutcomeForEvent(_ as List, _, _, _) >> Optional.of(events)
    this.consumeBirHREvents.consumeBirEvents() >> events
    Map<String, RacingFormOutcome> racingFormOutcomeMap = events.stream()
        .filter({ object -> object != null })
        .map({ children -> children.getRacingFormOutcome() })
        .filter({ object -> object != null })
        .filter({ rfo -> "outcome".equalsIgnoreCase(rfo.getRefRecordType()) })
        .collect(toMap({ racingFormOutcome -> racingFormOutcome.getRefRecordId() }, identity(), { a, b -> a }))


    // action
    racingDataInjector.injectData(racingDataInjector.toEventsModuleData(model), idsCollector)

    // results assertions
    model.getModules().stream()
        .map({ outputModule -> outputModule.getData() })
        .filter({ object -> object != null })
        .flatMap({ collection -> collection.stream() })
        .filter({ item -> item.getId() != null })
        .filter({ item -> item.getOutcomeId() == null })
        .filter({ item -> eventMap.containsKey(valueOf(item.getId())) })
        .forEach({ item ->
          Event event = eventMap.get(valueOf(item.getId()))
          assert DataToOutputData.verifyDataItem(item, event)

          EventsModuleData moduleData = model.getModules().get(3).getData().get(0)
          assert moduleData.getRacingFormEvent() != null

          Map<String, Market> eventMarkets = event.getMarkets().stream()
              .filter({ m -> m.getIsActive() && m.getIsAvailable() })
              .collect(toMap({ market -> market.getId() }, identity()))
          assert item.getMarkets().size() == eventMarkets.size()
          item.getMarkets().stream()
              .filter({ m -> eventMarkets.containsKey(m.getId()) })
              .forEach({ m ->
                Market market = eventMarkets.get(m.getId())
                assert DataToOutputData.verifyMarket(m, market)


                Map<String, Outcome> outcomes = market.getOutcomes().stream()
                    .collect(toMap({ outcome -> outcome.getId() }, identity()))
                m.getOutcomes().stream()
                    .filter({ o -> racingFormOutcomeMap.containsKey(o.getId()) })
                    .forEach({ o ->
                      RacingFormOutcome racingFormOutcome = racingFormOutcomeMap.get(o.getId())
                      assert DataToOutputData.verifyRacingFormOutcome(o, racingFormOutcome)
                    })
                m.getOutcomes().stream()
                    .filter({ o -> outcomes.containsKey(o.getId()) })
                    .forEach({ o ->
                      Outcome outcome = outcomes.get(o.getId())
                      assert DataToOutputData.verifyOutcome(o, outcome)


                      Map<String, Price> priceMap = outcome.getPrices().stream()
                          .collect(toMap({ price -> price.getId() }, identity()))
                      o.getPrices().stream()
                          .filter({ p -> priceMap.containsKey(p.getId()) })
                          .forEach({ p ->
                            Price price = priceMap.get(p.getId())
                            DataToOutputData.verifyPrice(p, price)
                          })
                    })
              })
        })
    expect:
    true
  }
}
