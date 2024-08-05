package com.coral.oxygen.middleware.featured.consumer.sportpage

import com.coral.oxygen.cms.api.CmsService
import com.coral.oxygen.middleware.common.service.featured.IdsCollector
import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector
import com.coral.oxygen.middleware.featured.service.injector.FeaturedCommentaryInjector
import com.coral.oxygen.middleware.featured.service.injector.MarketsCountInjector
import com.coral.oxygen.middleware.pojos.model.cms.Fanzone
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

class FanzoneHighlightCarouselModuleProcessorTest extends Specification {
  SiteServerApi siteServerApi
  EventDataInjector eventDataInjector
  MarketsCountInjector marketsCountInjector
  FeaturedCommentaryInjector commentaryInjector
  CmsService cmsService
  FanzoneHighlightCarouselModuleProcessor fZHProcessor

  def setup() {
    siteServerApi = Mock(SiteServerApi)
    eventDataInjector = Mock(EventDataInjector)
    marketsCountInjector = Mock(MarketsCountInjector)
    commentaryInjector = Mock(FeaturedCommentaryInjector)
    cmsService=Mock(CmsService)

    fZHProcessor = new FanzoneHighlightCarouselModuleProcessor(siteServerApi, eventDataInjector, marketsCountInjector, commentaryInjector, cmsService)
  }

  def "Process two HighlightCarousels with correct type and event ids should succeed"() {
    def firstCarousel = new HighlightCarousel()
    def firstCarouselEventIds = Arrays.asList("15454", "45746", "54645")
    def firstEventIdsLong = firstCarouselEventIds.stream().map({ sId -> new Long(Long.parseLong(sId)) }).collect()
    def firstCarouselFanzones = Arrays.asList("1234", "12345")
    firstCarousel.events = firstCarouselEventIds
    firstCarousel.typeIds = Arrays.asList("442","441","443")
    firstCarousel.sportId = 160
    firstCarousel.setInPlay(true)
    firstCarousel.displayOrder = 0
    firstCarousel.fanzoneSegments = firstCarouselFanzones
    firstCarousel.displayMarketType="Primary"
    def secondCarousel = new HighlightCarousel()
    def secondCarouselFanzones = Arrays.asList("1234", "12345")
    def secondCarouselEventIds = IntStream.range(0, 10)
        .mapToObj({ index -> RandomUtils.nextLong(100000000, 900000000)})
        .collect(Collectors.toList())
    secondCarousel.typeIds = Arrays.asList("442","441","443")
    secondCarousel.sportId = 160
    secondCarousel.setInPlay(true)
    secondCarousel.displayOrder = 1
    secondCarousel.fanzoneSegments = secondCarouselFanzones
    secondCarousel.displayMarketType="Primary"
    def sportPageModule = homePageWithHighlightCarousels(firstCarousel, secondCarousel)
    def fanzone1 = new Fanzone()
    fanzone1.name = "segment-one"
    fanzone1.primaryCompetitionId = "441"
    fanzone1.secondaryCompetitionId = "442,443"
    fanzone1.teamId = "1234"
    def fanzone2 = new Fanzone()
    fanzone2.name = "segment-two"
    fanzone2.primaryCompetitionId = "441"
    fanzone2.secondaryCompetitionId = "442,443"
    fanzone2.teamId = "12345"
    def fanzone3 = new Fanzone()
    fanzone3.name = "invalid"
    fanzone3.primaryCompetitionId = "441"
    fanzone3.secondaryCompetitionId = "442,443"
    fanzone3.teamId = "123456"
    def fanzones = Arrays.asList(fanzone1,fanzone2,fanzone3)
    cmsService.getFanzones() >> fanzones
    siteServerApi.getEventToOutcomeForEvent(*_) >>
        Optional.of(firstCarouselEventIds.stream()
        .map({ id ->
          def event = new Event(); event.id = id
          def che = new Children(); che.event = event; che
        })
        .collect()
        )

    siteServerApi.getEventForType(secondCarousel.typeIds, _ as SimpleFilter) >> Optional.of(
        secondCarouselEventIds.stream()
        .map({ id -> def event = new Event(); event.id = id; event })
        .collect()
        )

    eventDataInjector.injectData(_ as List<EventsModuleData>, _ as IdsCollector,"Primary" as String) >> { arguments ->
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
    def actual = fZHProcessor.processModules(sportPageModule, null, null) as List<HighlightCarouselModule>

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
  }

  def "Test live event is not returned when carousel show inplay is false"() {
    given:
    def carousel = new HighlightCarousel()
    def carouselFanzones = Arrays.asList("1234", "12345")
    carousel.setInPlay(Boolean.FALSE)
    carousel.fanzoneSegments= carouselFanzones
    carousel.events = Arrays.asList("15454", "45746", "54645")
    carousel.sportId = 160
    carousel.displayMarketType="Primary"
    def sportPageModule = homePageWithHighlightCarousels(carousel)
    def liveEventId = 15454
    def expectedIds = Arrays.asList(45746L, 54645L)
    def fanzone1 = new Fanzone()
    fanzone1.name = "segment-one"
    fanzone1.primaryCompetitionId = "441"
    fanzone1.secondaryCompetitionId = "442,443"
    fanzone1.teamId = "1234"
    def fanzone2 = new Fanzone()
    fanzone2.name = "segment-two"
    fanzone2.primaryCompetitionId = "441"
    fanzone2.secondaryCompetitionId = "442,443"
    fanzone2.teamId = "12345"
    def fanzones = Arrays.asList(fanzone1,fanzone2)
    cmsService.getFanzones() >> fanzones

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
    def actual = fZHProcessor.processModules(sportPageModule, null, null) as List<HighlightCarouselModule>

    then:
    actual.size() == 1
    actual.get(0).getData().size() == 2
    expectedIds.containsAll(actual.get(0).getEventIds())
    actual.get(0).getData().stream().allMatch({ event -> expectedIds.contains(event.getId()) })
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
    fZHProcessor.applyLimits(Arrays.asList(firstModule, secondModule))

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
  def "Process HighlightCarousel with FZ001 team id should succeed"() {
    def firstCarousel = new HighlightCarousel()
    def firstCarouselFanzones = Arrays.asList("1234", "12345")
    firstCarousel.events = Collections.emptyList()
    firstCarousel.typeIds = Arrays.asList("442","441","443")
    firstCarousel.sportId = 160
    firstCarousel.setInPlay(true)
    firstCarousel.displayOrder = 0
    firstCarousel.fanzoneSegments = firstCarouselFanzones
    firstCarousel.displayMarketType="Primary"
    def secondCarousel = new HighlightCarousel()
    def secondCarouselFanzones = Arrays.asList("FZ001")
    def secondCarouselEventIds = IntStream.range(0, 10)
        .mapToObj({ index -> RandomUtils.nextLong(100000000, 900000000)})
        .collect(Collectors.toList())
    secondCarousel.typeIds = Arrays.asList("442","441","443")
    secondCarousel.sportId = 160
    secondCarousel.setInPlay(true)
    secondCarousel.displayOrder = 1
    secondCarousel.fanzoneSegments = secondCarouselFanzones
    secondCarousel.displayMarketType="Primary"
    def sportPageModule = homePageWithHighlightCarousels(firstCarousel, secondCarousel)
    def fanzone1 = new Fanzone()
    fanzone1.name = "segment-one"
    fanzone1.primaryCompetitionId = "441"
    fanzone1.secondaryCompetitionId = "442,443"
    fanzone1.teamId = "1234"
    def fanzone2 = new Fanzone()
    fanzone2.name = "segment-two"
    fanzone2.primaryCompetitionId = "441"
    fanzone2.secondaryCompetitionId = "442,443"
    fanzone2.teamId = "12345"
    def fanzone3 = new Fanzone()
    fanzone3.name = "21team"
    fanzone3.primaryCompetitionId = "441"
    fanzone3.secondaryCompetitionId = "442,443"
    fanzone3.teamId = "FZ001"
    def fanzones = Arrays.asList(fanzone1,fanzone2,fanzone3)
    cmsService.getFanzones() >> fanzones
    siteServerApi.getEventForType(secondCarousel.typeIds, _ as SimpleFilter) >> Optional.of(
        secondCarouselEventIds.stream()
        .map({ id -> def event = new Event(); event.id = id; event })
        .collect()
        )
    eventDataInjector.injectData(_ as List<EventsModuleData>, _ as IdsCollector,"Primary" as String) >> { arguments ->
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
    def actual = fZHProcessor.processModules(sportPageModule, null, null) as List<HighlightCarouselModule>
    then:
    actual.size() == 2
  }
  private static SportPageModule homePageWithHighlightCarousels(HighlightCarousel... highlightCarousels) {
    def highlightCarouselModule = new SportModule()

    highlightCarouselModule.id = UUID.randomUUID().toString()
    highlightCarouselModule.moduleType = ModuleType.HIGHLIGHTS_CAROUSEL

    new SportPageModule(highlightCarouselModule, Arrays.asList(highlightCarousels))
  }
}
