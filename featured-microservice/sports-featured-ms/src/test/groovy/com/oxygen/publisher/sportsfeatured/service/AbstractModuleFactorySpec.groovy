package com.oxygen.publisher.sportsfeatured.service

import com.oxygen.publisher.configuration.JsonSupportConfig
import com.oxygen.publisher.model.OutputMarket
import com.oxygen.publisher.sportsfeatured.context.SportsMiddlewareContext
import com.oxygen.publisher.sportsfeatured.context.SportsSessionContext
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData
import com.oxygen.publisher.sportsfeatured.model.FeaturedModel
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex
import com.oxygen.publisher.sportsfeatured.model.module.AbstractFeaturedModule
import com.oxygen.publisher.sportsfeatured.model.module.EventsModule
import com.oxygen.publisher.sportsfeatured.model.module.InplayModule
import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.SportSegment
import com.oxygen.publisher.translator.DiagnosticService
import org.springframework.util.CollectionUtils
import spock.lang.Specification

class AbstractModuleFactorySpec extends Specification {

  private AbstractModuleFactory moduleFactory

  private SportsMiddlewareContext context
  private SportsCachedData sportsCachedData
  private DiagnosticService diagnosticService
  private SportsSessionContext sportsSessionContext;

  void setup() {
    context = Mock(SportsMiddlewareContext.class)
    sportsCachedData = Mock(SportsCachedData.class)
    context.getFeaturedCachedData() >> sportsCachedData

    diagnosticService = Mock(DiagnosticService)
    moduleFactory = new SportsChainFactory(context, new JsonSupportConfig().objectMapper(), diagnosticService,sportsSessionContext)
  }

  def "fixOldModule - check modules replacement"() {
    given: "new module received"
    EventsModule newModule = createEventsModule("42", newModuleName)
    and: "old module exists in structure cache"
    EventsModule oldModule = createEventsModule("42", oldModuleName)
    FeaturedModel structure = new FeaturedModel()
    structure.addModule(oldModule)
    sportsCachedData.getStructure(PageRawIndex.forSport(16)) >> structure

    expect:
    moduleFactory.fixOldModule(newModule, structure)
    List<AbstractFeaturedModule> modules = structure
        .getModules(newModule.getIdentifier())

    !CollectionUtils.isEmpty(modules)
    modules.get(0).getTitle() == newModuleName

    where:
    newModuleName << ["new_module", "same_module"]
    oldModuleName << ["old_module", "same_module"]
  }

  def "test modules order preserved after replacement"() {
    given: "new module received"
    EventsModule newModule = createEventsModule("1", newModuleName)
    and: "old module exists in structure cache"
    EventsModule oldModule1 = createEventsModule("1", oldModuleName)
    EventsModule oldModule2 = createEventsModule("2", oldModuleName)
    FeaturedModel structure = new FeaturedModel()
    structure.addModule(oldModule1)
    structure.addModule(oldModule2)
    sportsCachedData.getStructure(PageRawIndex.forSport(16)) >> structure

    expect:
    moduleFactory.fixOldModule(newModule, structure)
    List<AbstractFeaturedModule> modules = structure
        .getModules(newModule.getIdentifier())

    !CollectionUtils.isEmpty(modules)
    // first module should be replaced
    modules.get(0).getTitle() == newModuleName

    where:
    newModuleName << ["new_module", "same_module"]
    oldModuleName << ["old_module", "same_module"]
  }

  def "check unnecessary fields are cut for InPlay module"() {
    given:
    InplayModule module = new InplayModule()
    module.setTitle("some_title")
    module.setId("3453435352")
    module.setData(Arrays.asList(new SportSegment()))
    module.setTotalEvents(2)
    module.setSportId(16)
    module.setPublishedDevices(Arrays.asList("mobile"))
    module.setShowExpanded(Boolean.TRUE)

    when:
    InplayModule minifyModule = (InplayModule) moduleFactory.minifyModule(module)

    then:
    minifyModule.getId() == "3453435352"
    minifyModule.getTotalEvents() == 2
    minifyModule.getSportId() == 16

    CollectionUtils.isEmpty(minifyModule.getData())
    Objects.isNull(minifyModule.getPublishedDevices())
    Objects.isNull(minifyModule.getTitle())
    Objects.isNull(minifyModule.getShowExpanded())
  }

  def "verify feature module is not modified"() {
    given:
    EventsModule module = createEventsModule("42", "someTitle")

    when:
    EventsModule minifyModule = (EventsModule) moduleFactory.minifyModule(module)

    then:
    minifyModule.getId() == "42"
    minifyModule.getTotalEvents() == 1
    minifyModule.getSportId() == 16
    minifyModule.getTitle() == "someTitle"
    !CollectionUtils.isEmpty(minifyModule.getData())
  }


  private EventsModule createEventsModule(String id, String title) {
    EventsModule module = new EventsModule()
    module.setId(id)
    module.setTotalEvents(1)
    module.setSportId(16)
    module.setData(createEventsModuleData())
    module.setTitle(title)

    return module
  }

  private static List<EventsModuleData> createEventsModuleData() {
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
}
