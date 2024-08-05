package com.oxygen.publisher.sportsfeatured.service

import com.oxygen.publisher.configuration.JsonSupportConfig
import com.oxygen.publisher.model.OutputMarket
import com.oxygen.publisher.sportsfeatured.context.SportsMiddlewareContext
import com.oxygen.publisher.sportsfeatured.context.SportsSessionContext
import com.oxygen.publisher.sportsfeatured.model.FeaturedByEventMarket
import com.oxygen.publisher.sportsfeatured.model.ModuleType
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData
import com.oxygen.publisher.sportsfeatured.model.module.AbstractFeaturedModule
import com.oxygen.publisher.sportsfeatured.model.module.EventsModule
import com.oxygen.publisher.sportsfeatured.model.module.HighlightCarouselModule
import com.oxygen.publisher.sportsfeatured.model.module.InplayModule
import com.oxygen.publisher.sportsfeatured.model.module.PopularBetModule
import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData
import com.oxygen.publisher.sportsfeatured.model.module.data.PopularBetModuleData
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.SportSegment
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.TypeSegment
import com.oxygen.publisher.translator.DiagnosticService
import org.springframework.util.CollectionUtils
import spock.lang.Specification
import spock.lang.Unroll

import java.util.stream.Collectors

class AbstractSportsChainFactorySpec extends Specification {
  private AbstractSportsChainFactory factory

  private SportsMiddlewareContext context
  private SportsCachedData sportsCachedData
  private DiagnosticService diagnosticService
  private SportsSessionContext sportsSessionContext;

  void setup() {
    context = Mock(SportsMiddlewareContext.class)
    sportsCachedData = Mock(SportsCachedData.class)
    context.getFeaturedCachedData() >> sportsCachedData

    diagnosticService = Mock(DiagnosticService)
    factory = new SportsChainFactory(context, new JsonSupportConfig().objectMapper(), this.diagnosticService,sportsSessionContext)
  }

  @Unroll
  def "verify optimizeModule for module #moduleType with cache empty=#cacheEmpty"() {
    given: "new module received"
    AbstractFeaturedModule module = createModule(moduleType)

    and: "cache is being populated"
    FeaturedByEventMarket featuredByEventMarket = FeaturedByEventMarket.
        builder()
        .moduleData(new EventsModuleData())
        .primaryMarkets(new ArrayList<OutputMarket>())
        .build()
    Map<String, FeaturedByEventMarket> prMarketsCache = new HashMap<>()
    if (!cacheEmpty) {
      prMarketsCache.put("432267", featuredByEventMarket)
    }

    expect:
    Map<String, FeaturedByEventMarket> resultingCache =
        factory.optimizeModule(prMarketsCache, module)

    and: "data in cache is updated/created"
    !CollectionUtils.isEmpty(resultingCache)
    FeaturedByEventMarket updatedValue = resultingCache.get("432267")
    updatedValue != null
    updatedValue.getModuleIds().contains(moduleId)
    updatedValue.moduleData.getId() == "432267"
    !CollectionUtils.isEmpty(updatedValue.getPrimaryMarkets())

    and: "primary markets exist in original module"
    !CollectionUtils.isEmpty(getMarkets(module))

    where:
    moduleId | moduleType                     | cacheEmpty
    "42"     | ModuleType.FEATURED            | false
    "42"     | ModuleType.FEATURED            | true
    "27"     | ModuleType.IN_PLAY             | false
    "27"     | ModuleType.IN_PLAY             | true
    "31"     | ModuleType.HIGHLIGHTS_CAROUSEL | false
    "31"     | ModuleType.HIGHLIGHTS_CAROUSEL | true
    "88"     | ModuleType.POPULAR_BETS        | false
    "88"     | ModuleType.POPULAR_BETS        | true
  }

  private AbstractFeaturedModule createModule(ModuleType moduleType) {
    switch (moduleType) {
      case ModuleType.FEATURED: return createEventsModule()
      case ModuleType.IN_PLAY: return createInplayModule()
      case ModuleType.HIGHLIGHTS_CAROUSEL: return createCarouselModule()
      case ModuleType.POPULAR_BETS: return createPopularBetModule()
      default: return null
    }
  }

  private EventsModule createEventsModule() {
    EventsModule module = new EventsModule()
    module.setId("42")
    module.setTotalEvents(1)
    module.setSportId(16)
    module.setData(createEventsModuleData())
    module.setTitle("eventModule")

    return module
  }

  private InplayModule createInplayModule() {
    InplayModule module = new InplayModule()
    module.setId("27")
    module.setTitle("InPlayModule")
    List<SportSegment> sportSegments = new ArrayList<>()
    SportSegment sportSegment = new SportSegment()
    List<TypeSegment> typeSegments = new ArrayList<>()
    TypeSegment typeSegment = new TypeSegment()
    typeSegment.setEvents(createEventsModuleData())
    typeSegments.add(typeSegment)
    sportSegment.setEventsByTypeName(typeSegments)
    sportSegments.add(sportSegment)
    module.setData(sportSegments)

    return module
  }

  private PopularBetModule createPopularBetModule() {
    PopularBetModule module = new PopularBetModule()
    module.setId("88")
    module.setTitle("InPlayModule")
    module.setData(createPopularBetModuleData())

    return module
  }

  private HighlightCarouselModule createCarouselModule() {
    HighlightCarouselModule module = new HighlightCarouselModule()
    module.setId("31")
    module.setTotalEvents(1)
    module.setSportId(16)
    module.setData(createEventsModuleData())
    module.setTitle("carouselModule")

    return module
  }

  private List<EventsModuleData> createEventsModuleData() {
    List<EventsModuleData> moduleData = new ArrayList<>()

    EventsModuleData item = new EventsModuleData()
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

  private List<OutputMarket> getMarkets(AbstractFeaturedModule module) {
    switch (module.getModuleType()) {
      case ModuleType.FEATURED: return getPrimaryMarkets((EventsModule) module)
      case ModuleType.IN_PLAY: return getPrimaryMarkets((InplayModule) module)
      case ModuleType.HIGHLIGHTS_CAROUSEL: return getPrimaryMarkets((HighlightCarouselModule) module)
      case ModuleType.POPULAR_BETS: return getPrimaryMarkets((PopularBetModule)module)
      default: return null
    }
  }

  private List<OutputMarket> getPrimaryMarkets(HighlightCarouselModule module) {
    return getPrimaryMarkets((EventsModule) module);
  }

  private List<OutputMarket> getPrimaryMarkets(EventsModule module) {
    return module.getData().stream()
        .map { item -> item.getPrimaryMarkets() }
        .flatMap { markets -> markets.stream() }
        .collect(Collectors.toList())
  }

  private List<OutputMarket> getPrimaryMarkets(InplayModule module) {
    return module.getData().stream()
        .map { sportSegment -> sportSegment.getEventsByTypeName() }
        .flatMap { typeSegments -> typeSegments.stream() }
        .map { typeSegment -> typeSegment.getEvents() }
        .flatMap { data -> data.stream() }
        .map { item -> item.getPrimaryMarkets() }
        .flatMap { markets -> markets.stream() }
        .collect(Collectors.toList())
  }
}
