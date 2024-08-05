package com.coral.oxygen.middleware.featured.service


import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig
import com.coral.oxygen.middleware.pojos.model.cms.ModuleDataSelection
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome
import com.coral.oxygen.middleware.pojos.model.output.OutputPrice
import com.coral.oxygen.middleware.pojos.model.output.featured.EventsModule
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModel
import com.coral.oxygen.middleware.pojos.model.output.featured.SurfaceBetModule
import com.coral.oxygen.middleware.pojos.model.output.featured.SurfaceBetModuleData
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.Aggregation
import org.joda.time.DateTime
import spock.lang.Specification

import static com.coral.oxygen.middleware.pojos.model.cms.EventLoadingType.*

class FeaturedDataFilterSpec extends Specification {
  FeaturedDataFilter filter
  SiteServerApi siteServerApi

  def setup() {
    filter = new FeaturedDataFilter()
    siteServerApi = Mock(SiteServerApi)
    filter.setSiteServerApi(siteServerApi)
    siteServerApi.getMarketsCountForEvent(_, _) >> Optional.empty()
  }

  def "RacingGridModule is RacingGridModule"() {
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionType(RACING_GRID.getValue())

    expect:
    boolean result = filter.isRacingGridModule(dataSelection)
    result
  }

  def "NotRacingGridModule is not RacingGridModule"() {
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionType("SomeType")

    expect:
    boolean result = filter.isRacingGridModule(dataSelection)
    !result
  }

  def "Removing empty nodes in case when LP is present and SP is not present - should ignore when prices exist"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())

    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")

    EventsModule eventsModule = new EventsModule()
    EventsModuleData eventsModuleData = new EventsModuleData()
    eventsModule.setDataSelection(dataSelection)
    model.getModules().add(eventsModule)

    eventsModule.setData(new ArrayList<>())
    eventsModule.getData().add(eventsModuleData)

    OutputOutcome outcome = new OutputOutcome()
    outcome.setPrices(new ArrayList<>())
    outcome.getPrices().add(new OutputPrice())

    OutputMarket market = new OutputMarket()
    eventsModuleData.setMarkets(new ArrayList<>())
    eventsModuleData.getMarkets().add(market)
    // outcomes without prices should be removed in case when LP is present and SP is not present
    market.setPriceTypeCodes("LP")
    market.setOutcomes(new ArrayList<>())
    market.getOutcomes().add(outcome)

    expect:
    filter.removeEmptyNodes(model.getModules())
    1 == model.getModules().size()
    1 == eventsModule.getData().size()
    1 == eventsModuleData.getMarkets().size()
    1 == market.getOutcomes().size()
    1 == outcome.getPrices().size()
  }

  def "Removing empty nodes in case when LP is present and SP is not present - should remove when prices empty"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())

    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")

    EventsModule eventsModule = new EventsModule()
    eventsModule.setDataSelection(dataSelection)

    EventsModuleData eventsModuleData = new EventsModuleData()
    eventsModule.setData(new ArrayList<>())
    eventsModule.getData().add(eventsModuleData)

    model.getModules().add(eventsModule)

    def outcome = new OutputOutcome()
    outcome.setPrices(Collections.emptyList())

    // outcomes without prices should be removed in case when LP is present and SP is not present
    def market = new OutputMarket()
    market.setPriceTypeCodes("LP")
    market.setOutcomes(new ArrayList<>())
    market.getOutcomes().add(outcome)

    eventsModuleData.setMarkets(new ArrayList<>())
    eventsModuleData.getMarkets().add(market)

    expect:
    filter.removeEmptyNodes(model.getModules())
    model.getModules().isEmpty()
  }

  def "Removing empty nodes in case when LP is present and SP is not present - should remove when prices don't exist"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().add(new OutputMarket())
    // outcomes without prices should be removed in case when LP is present and SP is not present
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setPriceTypeCodes("LP")
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setOutcomes(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().get(0).getOutcomes().add(new OutputOutcome())

    expect:
    filter.removeEmptyNodes(model.getModules())
    model.getModules().size() == 0
  }

  def "Removing empty nodes in case when LP is present and SP is not present - empty outcomes list causes node to be removed"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().add(new OutputMarket())
    // outcomes without prices should be removed in case when LP is present and SP is not present
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setPriceTypeCodes("LP")
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setOutcomes(new ArrayList<>())

    expect:
    filter.removeEmptyNodes(model.getModules())
    model.getModules().size() == 0
  }

  def "Removing empty nodes in case when LP is present and SP is not present - absent outcomes list causes node to be removed"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().add(new OutputMarket())
    // outcomes without prices should be removed in case when LP is present and SP is not present
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setPriceTypeCodes("LP")

    expect:
    filter.removeEmptyNodes(model.getModules())
    model.getModules().size() == 0
  }

  def "Empty market list causes node to be removed"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())

    expect:
    filter.removeEmptyNodes(model.getModules())
    model.getModules().size() == 0
  }

  def "Null market list causes node to be removed"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())

    expect:
    filter.removeEmptyNodes(model.getModules())
    model.getModules().size() == 0
  }

  def "Empty module data causes node to be removed"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())

    expect:
    filter.removeEmptyNodes(model.getModules())
    model.getModules().size() == 0
  }

  def "Price typecode SP causes nodes not to be removed"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().add(new OutputMarket())
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setPriceTypeCodes("SP")
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setOutcomes(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().get(0).getOutcomes().add(new OutputOutcome())
    model.getModules().get(0).getData().get(0).getMarkets().get(0).getOutcomes().get(0).setPrices(new ArrayList<>())

    expect:
    filter.removeEmptyNodes(model.getModules())
    model.getModules().size() == 1
    model.getModules().get(0).getData().size() == 1
    model.getModules().get(0).getData().get(0).getMarkets().size() == 1
    model.getModules().get(0).getData().get(0).getMarkets().get(0).getOutcomes().size() == 1
    model.getModules().get(0).getData().get(0).getMarkets().get(0).getOutcomes().get(0).getPrices().size() == 0
  }

  def "Removing older events does not effect events occurring now"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setStartTime(DateTime.now().toString("yyyy-MM-dd'T'HH:mm:ssZ"))

    when:
    filter.setEventStartTimeInPastThresholdHours(2)
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig()
    cmsSystemConfig.setFeaturedCategoryIdEventDisplayHours(new HashMap<>())
    filter.removeOlderEvents(model.getModules(), cmsSystemConfig)

    then:
    model.getModules().size() == 1
    model.getModules().get(0).getData().size() == 1
  }

  def "Remove modules with error"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    EventsModule outputModule = new EventsModule()
    outputModule.setErrorMessage("")
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())

    when:
    filter.removeModulesWithError(model.getModules())

    then:
    model.getModules().size() == 0
  }


  def "Event in past removed properly"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setStartTime(DateTime.now().minusHours(3).toString("yyyy-MM-dd'T'HH:mm:ssZ"))

    when:
    filter.setEventStartTimeInPastThresholdHours(2)
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig()
    cmsSystemConfig.setFeaturedCategoryIdEventDisplayHours(new HashMap<>())
    filter.removeOlderEvents(model.getModules(), cmsSystemConfig)

    then:
    model.getModules().size() == 1
    model.getModules().get(0).getData().size() == 0
  }

  def "Event in past with millis format removed properly"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setStartTime(DateTime.now().minusHours(3).toString("yyyy-MM-dd'T'HH:mm:ss.sssZ"))

    when:
    filter.setEventStartTimeInPastThresholdHours(2)
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig()
    cmsSystemConfig.setFeaturedCategoryIdEventDisplayHours(new HashMap<>())
    filter.removeOlderEvents(model.getModules(), cmsSystemConfig)

    then:
    model.getModules().size() == 1
    model.getModules().get(0).getData().size() == 0
  }

  def "Remove older events with cms configuration for category"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setStartTime(DateTime.now().minusHours(96).toString("yyyy-MM-dd'T'HH:mm:ssZ"))
    model.getModules().get(0).getData().get(0).setCategoryId("16")

    when:
    filter.setEventStartTimeInPastThresholdHours(24)
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig()
    cmsSystemConfig.setFeaturedCategoryIdEventDisplayHours(new HashMap<>())
    cmsSystemConfig.getCategoryIdEventsTimeoutMap().put("16", 48)
    filter.removeOlderEvents(model.getModules(), cmsSystemConfig)

    then:
    model.getModules().size() == 1
    model.getModules().get(0).getData().size() == 0
  }

  def "Remove older events with cms configuration for category not occuring"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setStartTime(DateTime.now().minusHours(30).toString("yyyy-MM-dd'T'HH:mm:ssZ"))
    model.getModules().get(0).getData().get(0).setCategoryId("16")

    when:
    filter.setEventStartTimeInPastThresholdHours(24)
    CmsSystemConfig cmsSystemConfig = new CmsSystemConfig()
    cmsSystemConfig.setFeaturedCategoryIdEventDisplayHours(new HashMap<>())
    cmsSystemConfig.getCategoryIdEventsTimeoutMap().put("16", 48)
    filter.removeOlderEvents(model.getModules(), cmsSystemConfig)

    then:
    model.getModules().size() == 1
    model.getModules().get(0).getData().size() == 1
  }

  def "Remove not liveserved liveEvents is removing such events"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setEventIsLive(true)
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().add(new OutputMarket())
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setMarketBetInRun(false)
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setOutcomes(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().get(0).getOutcomes().add(new OutputOutcome())

    when:
    filter.removeNotLiveservedLiveEvents(model.getModules())

    then:
    model.getModules().get(0).getData().size() == 0
  }

  def "RemoveNotLiveservedLiveEvents skip notLiveEvents"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setEventIsLive(false)
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().add(new OutputMarket())
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setMarketBetInRun(false)
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setOutcomes(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().get(0).getOutcomes().add(new OutputOutcome())

    when:
    filter.removeNotLiveservedLiveEvents(model.getModules())

    then:
    model.getModules().get(0).getData().size() == 1
  }

  def "RemoveNotLiveservedLiveEvents skip liveserved liveEvents"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setEventIsLive(true)
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().add(new OutputMarket())
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setMarketBetInRun(true)
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setOutcomes(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().get(0).getOutcomes().add(new OutputOutcome())

    when:
    filter.removeNotLiveservedLiveEvents(model.getModules())

    then:
    model.getModules().get(0).getData().size() == 1
  }

  // ****************************
  // PHX-385 test section start
  // ****************************


  def "Pre-match event without markets not filtered"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setEventSortCode("MTCH")
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())

    when:
    filter.removeEmptyNodes(model.getModules())

    then:
    model.getModules().get(0).getData().size() == 1
  }

  def "Not MTCH event without market removed"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())

    when:
    filter.removeEmptyNodes(model.getModules())

    then:
    model.getModules().size() == 0
  }

  def "Pre-match event without outcomes removed"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setEventSortCode("MTCH")
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().add(new OutputMarket())
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setPriceTypeCodes("LP")

    when:
    filter.removeEmptyNodes(model.getModules())

    then:
    model.getModules().size() == 0
  }

  def "In-play events without outcomes removed"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setId(15L)
    model.getModules().get(0).getData().get(0).setEventSortCode("MTCH")
    model.getModules().get(0).getData().get(0).setDrilldownTagNames("EVFLAG_BL")
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().add(new OutputMarket())
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setPriceTypeCodes("LP")

    // there is one BetInRun market
    List<Aggregation> aggregations = new ArrayList<>()
    Aggregation aggregation = new Aggregation()
    aggregations.add(aggregation)
    aggregation.setRefRecordId(15L)
    aggregation.setCount(1)
    // primary market is BetInRun (the same)
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setMarketBetInRun(true)

    when:
    filter.removeEmptyNodes(model.getModules())

    then:
    siteServerApi.getMarketsCountForEvent(_, _) >> Optional.of(aggregations)
    model.getModules().size() == 0
  }

  def "In-play event without outcomes not filtered as there is another bet-in-run-market"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setId(15L)
    model.getModules().get(0).getData().get(0).setEventSortCode("MTCH")
    model.getModules().get(0).getData().get(0).setDrilldownTagNames("EVFLAG_BL")
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().add(new OutputMarket())
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setPriceTypeCodes("LP")

    // there is one BetInRun
    List<Aggregation> aggregations = createSSAggregationResponse(15L, 1)
    // primary market is not BetInRun (other market)
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setMarketBetInRun(false)

    when:
    filter.removeEmptyNodes(model.getModules())

    then:
    siteServerApi.getMarketsCountForEvent(_, _) >> Optional.of(aggregations)
    model.getModules().get(0).getData().size() == 1
  }

  def "In-play SurfaceBet with outcomes and not bet-in-run market is removed"() {
    given:
    SurfaceBetModuleData data = new SurfaceBetModuleData();
    data.setId(15L)
    data.setEventSortCode("MTCH")
    data.setDrilldownTagNames("EVFLAG_BL")
    data.setEventIsLive(true)
    data.setMarkets(Collections.singletonList(new OutputMarket()))
    data.getMarkets().get(0).setPriceTypeCodes("LP")
    data.getMarkets().get(0).setMarketBetInRun(false)
    def price = new OutputPrice()
    price.setPriceType("LP")
    price.setId("123")
    price.setPriceDec(2)
    price.setPriceNum(1)
    price.setPriceDen(3)
    data.getMarkets().get(0).setOutcomes(Collections.singletonList(new OutputOutcome()))
    data.getMarkets().get(0).getOutcomes().get(0).setPrices(Collections.singletonList(price))

    SurfaceBetModule outputModule = new SurfaceBetModule()
    def sbData = new ArrayList()
    sbData.add(data)
    outputModule.setData(sbData)

    def eventModules = Collections.singletonList(outputModule)

    when:
    // there is one BetInRun
    siteServerApi.getMarketsCountForEvent(*_) >> Optional.of(createSSAggregationResponse(15L, 1))

    then:
    filter.removeNotLiveservedLiveEvents(eventModules)
    eventModules.get(0).getData().size() == 0
  }

  private static ArrayList<Aggregation> createSSAggregationResponse(Long refId, Integer expectedCount) {
    List<Aggregation> aggregations = new ArrayList<>()
    Aggregation aggregation = new Aggregation()
    aggregations.add(aggregation)
    aggregation.setRefRecordId(refId)
    aggregation.setCount(expectedCount)
    aggregations
  }

  def "In-play event without outcomes not removed"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setId(15L)
    model.getModules().get(0).getData().get(0).setEventSortCode("MTCH")
    model.getModules().get(0).getData().get(0).setDrilldownTagNames("EVFLAG_BL")
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())
    model.getModules().get(0).getData().get(0).getMarkets().add(new OutputMarket())
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setPriceTypeCodes("LP")

    // there is two BetInRun markets
    List<Aggregation> aggregations = new ArrayList<>()
    Aggregation aggregation = new Aggregation()
    aggregations.add(aggregation)
    aggregation.setRefRecordId(15L)
    aggregation.setCount(2)
    // primary market is BetInRun (one of two)
    model.getModules().get(0).getData().get(0).getMarkets().get(0).setMarketBetInRun(true)

    when:
    filter.removeEmptyNodes(model.getModules())

    then:
    siteServerApi.getMarketsCountForEvent(_, _) >> Optional.of(aggregations)
    model.getModules().get(0).getData().size() == 1
  }

  def "In-play event without markets removed"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setId(15L)
    model.getModules().get(0).getData().get(0).setEventSortCode("MTCH")
    model.getModules().get(0).getData().get(0).setDrilldownTagNames("EVFLAG_BL")
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())

    // there is one BetInRun market
    List<Aggregation> aggregations = new ArrayList<>()
    Aggregation aggregation = new Aggregation()
    aggregations.add(aggregation)
    aggregation.setRefRecordId(15L)
    aggregation.setCount(0)

    when:
    filter.removeEmptyNodes(model.getModules())

    then:
    siteServerApi.getMarketsCountForEvent(_, _) >> Optional.of(aggregations)
    model.getModules().size() == 0
  }

  def "In-play event without markets not filtered as there is another bet-in-run-market"() {
    FeaturedModel model = new FeaturedModel()
    model.setModules(new ArrayList<>())
    ModuleDataSelection dataSelection = new ModuleDataSelection()
    dataSelection.setSelectionId("test")
    dataSelection.setSelectionType("test")
    EventsModule outputModule = new EventsModule()
    outputModule.setDataSelection(dataSelection)
    model.getModules().add(outputModule)
    model.getModules().get(0).setData(new ArrayList<>())
    model.getModules().get(0).getData().add(new EventsModuleData())
    model.getModules().get(0).getData().get(0).setId(15L)
    model.getModules().get(0).getData().get(0).setEventSortCode("MTCH")
    model.getModules().get(0).getData().get(0).setDrilldownTagNames("EVFLAG_BL")
    model.getModules().get(0).getData().get(0).setMarkets(new ArrayList<>())

    // there is one BetInRun
    List<Aggregation> aggregations = new ArrayList<>()
    Aggregation aggregation = new Aggregation()
    aggregations.add(aggregation)
    aggregation.setRefRecordId(15L)
    aggregation.setCount(1)

    when:
    filter.removeEmptyNodes(model.getModules())

    then:
    siteServerApi.getMarketsCountForEvent(_, _) >> Optional.of(aggregations)
    model.getModules().get(0).getData().size() == 1
  }
}
