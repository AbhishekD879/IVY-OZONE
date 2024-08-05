package com.coral.oxygen.middleware.featured.consumer.sportpage


import com.coral.oxygen.middleware.common.service.featured.IdsCollector
import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector
import com.coral.oxygen.middleware.featured.service.injector.FeaturedCommentaryInjector
import com.coral.oxygen.middleware.featured.service.injector.MarketsCountInjector
import com.coral.oxygen.middleware.pojos.model.cms.featured.HighlightCarousel
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome
import com.coral.oxygen.middleware.pojos.model.output.OutputPrice
import com.coral.oxygen.middleware.pojos.model.output.featured.HighlightCarouselModule
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType
import com.egalacoral.spark.siteserver.api.SimpleFilter
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.Children
import com.egalacoral.spark.siteserver.model.Event
import org.apache.commons.lang3.RandomUtils
import spock.lang.Specification

import java.util.stream.Collectors
import java.util.stream.IntStream

class HighlightCarouselModuleProcessorTest extends Specification {
  SiteServerApi siteServerApi
  EventDataInjector eventDataInjector
  MarketsCountInjector marketsCountInjector
  FeaturedCommentaryInjector commentaryInjector

  HighlightCarouselModuleProcessor highlightCarouselModuleProcessor

  def setup() {
    siteServerApi = Mock(SiteServerApi)
    eventDataInjector = Mock(EventDataInjector)
    marketsCountInjector = Mock(MarketsCountInjector)
    commentaryInjector = Mock(FeaturedCommentaryInjector)

    highlightCarouselModuleProcessor = new HighlightCarouselModuleProcessor(siteServerApi, eventDataInjector, marketsCountInjector, commentaryInjector)
  }

  def "Process two HighlightCarousels with correct type and event ids should succeed"() {
    def firstCarousel = new HighlightCarousel()
    def firstCarouselEventIds = Arrays.asList("15454", "45746", "54645")
    def firstEventIdsLong = firstCarouselEventIds.stream().map({ sId -> new Long(Long.parseLong(sId)) }).collect()

    firstCarousel.events = firstCarouselEventIds
    firstCarousel.sportId = 0
    firstCarousel.setInPlay(true)
    firstCarousel.displayOrder = 0
    firstCarousel.displayMarketType="Primary"
    def secondCarousel = new HighlightCarousel()
    def secondCarouselEventIds = IntStream.range(0, 10)
        .mapToObj({ index -> RandomUtils.nextLong(100000000, 900000000)})
        .collect(Collectors.toList())
    secondCarousel.typeId = 777
    secondCarousel.sportId = 0
    secondCarousel.setInPlay(true)
    secondCarousel.displayOrder = 1
    secondCarousel.displayMarketType="Primary"
    def sportPageModule = homePageWithHighlightCarousels(firstCarousel, secondCarousel)

    siteServerApi.getEventToOutcomeForEvent(*_) >>
        Optional.of(firstCarouselEventIds.stream()
        .map({ id ->
          def event = new Event(); event.id = id
          def che = new Children(); che.event = event; che
        })
        .collect()
        )

    siteServerApi.getEventForType(secondCarousel.typeId.toString(), _ as SimpleFilter) >> Optional.of(
        secondCarouselEventIds.stream()
        .map({ id -> def event = new Event(); event.id = id; event })
        .collect()
        )

    eventDataInjector.injectData(_ as List<EventsModuleData>, _ as IdsCollector ,"Primary" as String) >> { arguments ->
      (arguments[0] as List)
          .forEach { event ->
            def outcome = new OutputOutcome()
            outcome.setPrices(Collections.singletonList(new OutputPrice()))
            def market = new OutputMarket()
            market.setOutcomes(Collections.singletonList(outcome))
            (event as EventsModuleData).markets = Collections.singletonList(market)
          }
    }

    when:
    def actual = highlightCarouselModuleProcessor.processModules(sportPageModule, null, null) as List<HighlightCarouselModule>

    then:
    actual.size() == 2
    actual.stream()
        .filter({ module -> module.getEventIds().containsAll(firstEventIdsLong) })
        .findFirst()
        .map({ module -> module.getData() })
        .filter({ data -> data.size() == firstCarouselEventIds.size() })
        .map({ data ->
          data.stream()
              .allMatch({ dataItem -> firstEventIdsLong.contains(dataItem.getId()) })
        })
        .orElse(false)

    actual.stream()
        .filter({ module -> (secondCarousel.typeId == module.getTypeId()) })
        .findFirst()
        .map({ module -> module.getData() })
        .filter({ data -> data.size() == secondCarouselEventIds.size() })
        .map({ data ->
          data.stream()
              .allMatch({ dataItem -> secondCarouselEventIds.contains(dataItem.getId()) })
        })
        .orElse(false)
  }

  def "Test live event is not returned when carousel show inplay is false"() {
    given:
    def carousel = new HighlightCarousel()
    carousel.setInPlay(Boolean.FALSE)

    carousel.events = Arrays.asList("15454", "45746", "54645")
    carousel.sportId = 0
    carousel.displayMarketType="Primary"
    def sportPageModule = homePageWithHighlightCarousels(carousel)
    def liveEventId = 15454
    def expectedIds = Arrays.asList(45746L, 54645L)

    siteServerApi.getEventToOutcomeForEvent(*_) >>
        Optional.of(Arrays.asList("15454", "45746", "54645").stream()
        .map({ id ->
          def event = new Event(); event.id = id
          def che = new Children(); che.event = event; che
        })
        .collect()
        )

    eventDataInjector.injectData(_ as List<EventsModuleData>, _ as IdsCollector,"Primary" as String) >> { arguments ->
      (arguments[0] as List).forEach { i ->
        def outcome = new OutputOutcome()
        outcome.setPrices(Collections.singletonList(new OutputPrice()))
        def market = new OutputMarket()
        market.setOutcomes(Collections.singletonList(outcome))
        def event = i as EventsModuleData
        event.markets = Collections.singletonList(market)

        if (event.id == liveEventId) event.eventIsLive = Boolean.TRUE
      }
    }

    when:
    def actual = highlightCarouselModuleProcessor.processModules(sportPageModule, null, null) as List<HighlightCarouselModule>

    then:
    actual.size() == 1
    actual.get(0).getData().size() == 2
    expectedIds.containsAll(actual.get(0).getEventIds())
    actual.get(0).getData().stream().allMatch({ event -> expectedIds.contains(event.getId()) })
  }

  def "Test live event is not returned when carousel show inplay is false1"() {
    given:
    def carousel = new HighlightCarousel()
    carousel.setInPlay(Boolean.FALSE)
    carousel.displayMarketType="Primary"
    carousel.events = Arrays.asList("15454", "45746", "54645")
    carousel.sportId = 0
    def sportPageModule = homePageWithHighlightCarousels(carousel)
    def liveEventId = 15454
    def drilldowntagnames = "EVFLAG_BL,EVFLAG"

    siteServerApi.getEventToOutcomeForEvent(*_) >>
        Optional.of(Arrays.asList("15454", "45746", "54645").stream()
        .map({ id ->
          def event = new Event();
          event.id = id
          event.drilldownTagNames = drilldowntagnames
          event.isLiveNowEvent = Boolean.TRUE
          event.isStarted = Boolean.TRUE

          def che = new Children(); che.event = event; che
        })
        .collect()
        )

    eventDataInjector.injectData(_ as List<EventsModuleData>, _ as IdsCollector,"Primary" as String) >> { arguments ->
      (arguments[0] as List).forEach { i ->
        def outcome = new OutputOutcome()
        outcome.setPrices(Collections.singletonList(new OutputPrice()))
        def market = new OutputMarket()
        market.setOutcomes(Collections.singletonList(outcome))
        def event = i as EventsModuleData
        event.markets = Collections.singletonList(market)

        if (event.id == liveEventId)
          event.eventIsLive = Boolean.TRUE
      }
    }

    when:
    def actual = highlightCarouselModuleProcessor.processModules(sportPageModule, null, null) as List<HighlightCarouselModule>

    then:
    actual.size() == 1
    actual.get(0).getData().size() == 0
  }

  def "Test live event is not returned when carousel show inplay is false2"() {
    given:
    def carousel = new HighlightCarousel()
    carousel.setInPlay(Boolean.FALSE)
    carousel.displayMarketType="Primary"
    carousel.events = Arrays.asList("15454", "45746", "54645")
    carousel.sportId = 0
    def sportPageModule = homePageWithHighlightCarousels(carousel)
    def liveEventId = 15454
    def drilldowntagnames = "EVFLAG,EVE"

    siteServerApi.getEventToOutcomeForEvent(*_) >>
        Optional.of(Arrays.asList("15454", "45746", "54645").stream()
        .map({ id ->
          def event = new Event();
          event.id = id
          event.drilldownTagNames = drilldowntagnames
          event.isLiveNowEvent = Boolean.FALSE
          event.isStarted = Boolean.FALSE

          def che = new Children(); che.event = event; che
        })
        .collect()
        )

    eventDataInjector.injectData(_ as List<EventsModuleData>, _ as IdsCollector,"Primary" as String) >> { arguments ->
      (arguments[0] as List).forEach { i ->
        def outcome = new OutputOutcome()
        outcome.setPrices(Collections.singletonList(new OutputPrice()))
        def market = new OutputMarket()
        market.setOutcomes(Collections.singletonList(outcome))
        def event = i as EventsModuleData
        event.markets = Collections.singletonList(market)

        if (event.id == liveEventId)
          event.eventIsLive = Boolean.TRUE
      }
    }

    when:
    def actual = highlightCarouselModuleProcessor.processModules(sportPageModule, null, null) as List<HighlightCarouselModule>

    then:
    actual.size() == 1
    actual.get(0).getData().size() == 2
  }

  def "Test live event is not returned when carousel show inplay is false3"() {
    given:
    def carousel = new HighlightCarousel()
    carousel.setInPlay(Boolean.FALSE)
    carousel.displayMarketType="Primary"
    carousel.events = Arrays.asList("15454", "45746", "54645")
    carousel.sportId = 0
    def sportPageModule = homePageWithHighlightCarousels(carousel)
    def liveEventId = 15454
    def drilldowntagnames = "EVFLAG_BL,EVFLAG"

    siteServerApi.getEventToOutcomeForEvent(*_) >>
        Optional.of(Arrays.asList("15454", "45746", "54645").stream()
        .map({ id ->
          def event = new Event();
          event.id = id
          event.drilldownTagNames = drilldowntagnames
          event.isLiveNowEvent = Boolean.FALSE
          event.isStarted = Boolean.FALSE

          def che = new Children(); che.event = event; che
        })
        .collect()
        )

    eventDataInjector.injectData(_ as List<EventsModuleData>, _ as IdsCollector,"Primary" as String) >> { arguments ->
      (arguments[0] as List).forEach { i ->
        def outcome = new OutputOutcome()
        outcome.setPrices(Collections.singletonList(new OutputPrice()))
        def market = new OutputMarket()
        market.setOutcomes(Collections.singletonList(outcome))
        def event = i as EventsModuleData
        event.markets = Collections.singletonList(market)

        if (event.id == liveEventId)
          event.eventIsLive = Boolean.TRUE
      }
    }

    when:
    def actual = highlightCarouselModuleProcessor.processModules(sportPageModule, null, null) as List<HighlightCarouselModule>

    then:
    actual.size() == 1
    actual.get(0).getData().size() == 2
  }

  def "Test live event is not returned when carousel show inplay is false4"() {
    given:
    def carousel = new HighlightCarousel()
    carousel.setInPlay(Boolean.FALSE)
    carousel.displayMarketType="Primary"
    carousel.events = Arrays.asList("15454", "45746", "54645")
    carousel.sportId = 0
    def sportPageModule = homePageWithHighlightCarousels(carousel)
    def liveEventId = 15454
    def drilldowntagnames = "EVFLAG_BL,EVFLAG"

    siteServerApi.getEventToOutcomeForEvent(*_) >>
        Optional.of(Arrays.asList("15454", "45746", "54645").stream()
        .map({ id ->
          def event = new Event();
          event.id = id
          event.drilldownTagNames = drilldowntagnames
          event.isLiveNowEvent = Boolean.TRUE
          event.isStarted = Boolean.FALSE

          def che = new Children(); che.event = event; che
        })
        .collect()
        )

    eventDataInjector.injectData(_ as List<EventsModuleData>, _ as IdsCollector,"Primary" as String) >> { arguments ->
      (arguments[0] as List).forEach { i ->
        def outcome = new OutputOutcome()
        outcome.setPrices(Collections.singletonList(new OutputPrice()))
        def market = new OutputMarket()
        market.setOutcomes(Collections.singletonList(outcome))
        def event = i as EventsModuleData
        event.markets = Collections.singletonList(market)

        if (event.id == liveEventId)
          event.eventIsLive = Boolean.TRUE
      }
    }

    when:
    def actual = highlightCarouselModuleProcessor.processModules(sportPageModule, null, null) as List<HighlightCarouselModule>

    then:
    actual.size() == 1
    actual.get(0).getData().size() == 2
  }

  def "Apply limits on HighlightCarouselModule should succeed"() {
    def firstModuleData = IntStream.range(0, 15)
        .mapToObj({ index -> def event = new EventsModuleData(); event.setId(index); event })
        .collect(Collectors.toList())
    def secondModuleData = IntStream.range(0, 20)
        .mapToObj({ index -> def event = new EventsModuleData(); event.setId(index); event })
        .collect(Collectors.toList())
    def firstModule = new HighlightCarouselModule()
    firstModule.setLimit(10)
    firstModule.setData(firstModuleData)

    def secondModule = new HighlightCarouselModule()
    secondModule.setLimit(5)
    secondModule.setData(secondModuleData)

    when:
    highlightCarouselModuleProcessor.applyLimits(Arrays.asList(firstModule, secondModule))

    then:
    firstModule.getData().size() == firstModule.getLimit()
    firstModule.getData()
        .stream()
        .map({ dataItem -> dataItem.getId() })
        .allMatch({ id -> id >= 0 && id < firstModule.getLimit() })
    secondModule.getData().size() == secondModule.getLimit()
    secondModule.getData()
        .stream()
        .map({ dataItem -> dataItem.getId() })
        .allMatch({ id -> id >= 0 && id < secondModule.getLimit() })
  }

  private static SportPageModule homePageWithHighlightCarousels(HighlightCarousel... highlightCarousels) {
    def highlightCarouselModule = new SportModule()

    highlightCarouselModule.id = UUID.randomUUID().toString()
    highlightCarouselModule.moduleType = ModuleType.HIGHLIGHTS_CAROUSEL

    new SportPageModule(highlightCarouselModule, Arrays.asList(highlightCarousels))
  }
}
