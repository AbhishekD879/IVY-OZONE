package com.coral.oxygen.middleware.featured.consumer.sportpage

import static com.coral.oxygen.middleware.featured.utils.FeaturedDataUtils.getModularContentItemsFromResource

import com.coral.oxygen.cms.api.SystemConfigProvider
import com.coral.oxygen.middleware.common.service.featured.IdsCollector
import com.coral.oxygen.middleware.featured.service.BybService
import com.coral.oxygen.middleware.featured.service.FeaturedDataFilter
import com.coral.oxygen.middleware.featured.service.injector.DFRacingEventsModuleInjector
import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector
import com.coral.oxygen.middleware.featured.service.injector.FeaturedCommentaryInjector
import com.coral.oxygen.middleware.featured.service.injector.MarketsCountInjector
import com.coral.oxygen.middleware.featured.service.injector.RacingEventsModuleInjector
import com.coral.oxygen.middleware.featured.service.injector.SingleOutcomeEventsModuleInjector
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContent
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContentItem
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome
import com.coral.oxygen.middleware.pojos.model.output.featured.EventsModule
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType
import java.security.SecureRandom
import java.util.stream.Collectors
import spock.lang.Specification
import spock.lang.Unroll

class FeaturedModuleProcessorSpec extends Specification {

  FeaturedModuleProcessor moduleProcessor

  EventDataInjector eventDataInjector
  SingleOutcomeEventsModuleInjector singleOutcomeDataInjector
  RacingEventsModuleInjector racingDataInjector
  MarketsCountInjector marketsCountInjector
  FeaturedCommentaryInjector commentaryInjector
  SystemConfigProvider systemConfigProvider
  CmsSystemConfig cmsSystemConfig
  FeaturedDataFilter featuredDataFilter
  BybService bybService
  DFRacingEventsModuleInjector dfRacingEventsModuleInjector

  def setup() {
    systemConfigProvider = Mock(SystemConfigProvider)
    cmsSystemConfig = Mock(CmsSystemConfig)
    systemConfigProvider.systemConfig() >> cmsSystemConfig
    eventDataInjector = Mock(EventDataInjector)
    singleOutcomeDataInjector = Mock(SingleOutcomeEventsModuleInjector)
    racingDataInjector = Mock(RacingEventsModuleInjector)
    marketsCountInjector = Mock(MarketsCountInjector)
    commentaryInjector = Mock(FeaturedCommentaryInjector)
    featuredDataFilter = Mock(FeaturedDataFilter)
    bybService = Mock(BybService)
    dfRacingEventsModuleInjector = Mock(DFRacingEventsModuleInjector)

    moduleProcessor = new FeaturedModuleProcessor(eventDataInjector,
        singleOutcomeDataInjector, racingDataInjector, marketsCountInjector,
        commentaryInjector, featuredDataFilter, systemConfigProvider, bybService, dfRacingEventsModuleInjector)
  }

  @Unroll
  def "Check YC availability for drilldownTags #tagNames & byb availability #bybAvailable "() {
    given:
    SportModule sportModule = createSportModule()

    and: 'we have module with event with YourCall tag'
    ModularContent modularContent = getModularContentMock()
    ModularContentItem modularContentItem = getModularContentItem(modularContent)
    String tagModuleTitle = 'Type 442'

    and: 'module with dataSelection = Type'
    modularContentItem.getModules().stream()
        .filter { module -> module.getTitle().equalsIgnoreCase(tagModuleTitle) }
        .findFirst()
        .ifPresent { module ->
          module.getData().get(0)
              .setDrilldownTagNames(tagNames)
          module.getData().get(1)
              .setDrilldownTagNames('EVFLAG_PDM,EVFLAG_BL')
        }

    and:
    bybService.isBuildYourBetAvailableForType(442l) >> bybAvailable

    expect:
    List<EventsModule> modules = moduleProcessor
        .getFirstFeaturedEventModules(sportModule, modularContent, Collections.emptySet())

    def eventsModule = modules.stream()
        .filter { module -> module.getTitle().equalsIgnoreCase(tagModuleTitle) }
        .findFirst().get()

    eventsModule.isYourCallAvailable() == ycAvailability

    where:
    tagNames                         | bybAvailable || ycAvailability
    'EVFLAG_PDM,EVFLAG_BL,EVFLAG_YC' | false        || true
    'EVFLAG_PDM,EVFLAG_BL'           | false        || false
    'EVFLAG_PDM,EVFLAG_BL'           | true         || true
  }

  def "Check when Racing Data Hub was not defined"() {
    given:
    cmsSystemConfig = new CmsSystemConfig()
    systemConfigProvider.systemConfig() >> cmsSystemConfig
    SportModule sportModule = createSportModule()

    and:
    ModularContent modularContent = getModularContentMock()

    and:
    Set<Long> excludedEventIds = new HashSet<>(Arrays.asList(5850851l, 5851237l, 5843732l, 5804821l))

    when:
    List<EventsModule> modules = moduleProcessor
        .getFirstFeaturedEventModules(sportModule, modularContent, excludedEventIds)

    then:
    0 * dfRacingEventsModuleInjector.injectData(_, _)
  }

  def "Check when Racing Data Hub is enabled"() {
    given:
    cmsSystemConfig.hasRacingDataHub() >> Boolean.TRUE
    SportModule sportModule = createSportModule()

    and:
    ModularContent modularContent = getModularContentMock()

    and:
    Set<Long> excludedEventIds = new HashSet<>(Arrays.asList(5850851l, 5851237l, 5843732l, 5804821l))

    when:
    List<EventsModule> modules = moduleProcessor
        .getFirstFeaturedEventModules(sportModule, modularContent, excludedEventIds)

    then:
    (1.._) * dfRacingEventsModuleInjector.injectData(_, _)
  }

  def "Check when Racing Data Hub is disabled"() {
    given:
    cmsSystemConfig.hasRacingDataHub() >> Boolean.FALSE
    SportModule sportModule = createSportModule()

    and:
    ModularContent modularContent = getModularContentMock()

    and:
    Set<Long> excludedEventIds = new HashSet<>(Arrays.asList(5850851l, 5851237l, 5843732l, 5804821l))

    when:
    List<EventsModule> modules = moduleProcessor
        .getFirstFeaturedEventModules(sportModule, modularContent, excludedEventIds)

    then:
    0 * dfRacingEventsModuleInjector.injectData(_, _)
  }

  def "Check event exclusion"() {
    given:
    SportModule sportModule = createSportModule()
    sportModule.setSportId(16)

    and:
    ModularContent modularContent = getModularContentMock()

    and:
    Set<Long> excludedEventIds = new HashSet<>(Arrays.asList(5850851l, 5851237l, 5843732l, 5804821l))

    when:
    List<EventsModule> modules = moduleProcessor
        .getFirstFeaturedEventModules(sportModule, modularContent, excludedEventIds)

    then:
    Set<Long> idsSet = modules.stream()
        .flatMap { module -> module.getData().stream() }
        .map { data -> data.getId() }
        .collect(Collectors.toSet())

    !idsSet.containsAll(excludedEventIds)
  }

  def "Check eventName is overridden by outcome name for modules with Outcome data selection"() {
    given:
    SportModule sportModule = createSportModule()
    ModularContent modularContent = getModularContentMock()
    def outcomeName = 'Outcome name'
    def eventName = 'Event name'

    and:
    singleOutcomeDataInjector.injectData(*_) >> { List<EventsModuleData> events, IdsCollector idsCollector ->
      events.stream()
          .filter({ e -> e.getOutcomeId() != null }).forEach({ e -> fillSiteServeData(e, eventName, outcomeName) })
    }

    when:
    def actualModules = moduleProcessor.getFirstFeaturedEventModules(sportModule, modularContent, Collections.emptySet())

    then:
    !actualModules.isEmpty()
    def outcomeEvents = (actualModules as List<EventsModule>).stream()
        .flatMap({ m -> m.getData().stream().filter({ e -> Objects.nonNull(e.getOutcomeId()) }) }).collect(Collectors.toList())
    !outcomeEvents.isEmpty()
    outcomeEvents.stream().allMatch({ e -> e.getName().equals(outcomeName) })
  }

  def fillSiteServeData(EventsModuleData eventsModuleData, String eventName, String outcomeName) {
    def random = new SecureRandom()

    def outcome = new OutputOutcome()
    outcome.setId(String.valueOf(random.nextInt()))
    outcome.setName(outcomeName)

    def market = new OutputMarket()
    market.setId(String.valueOf(random.nextInt(1000)))
    market.setOutcomes(Collections.singletonList(outcome))

    eventsModuleData.setId(random.nextInt(1000))
    eventsModuleData.setName(eventName)
    eventsModuleData.setNameOverride(null)
    eventsModuleData.setStarted(Boolean.FALSE)
    eventsModuleData.setMarkets(Arrays.asList(market))
  }

  private ModularContentItem getModularContentItem(ModularContent modularContent) {
    modularContent.stream()
        .filter { item -> item.getDirectiveName().equalsIgnoreCase('Featured') }
        .findFirst().orElse(null)
  }

  private SportModule createSportModule() {
    SportModule sportModule = new SportModule()
    sportModule.setTitle('Featured module')
    sportModule.setPublishedDevices(new ArrayList<String>())
    sportModule.setSportId(0)
    sportModule.setId('353tgegse5t35dd55')
    sportModule.setModuleType(ModuleType.FEATURED)
    sportModule.setSortOrder(0.0)
    return sportModule
  }

  def "Check eventHub featured module"() {
    given:
    SportModule sportModule = createSportModule()
    ModularContent modularContent = getModularContentEventHubMock()
    def outcomeName = 'Outcome name'
    def eventName = 'Event name'

    and:
    singleOutcomeDataInjector.injectData(*_) >> { List<EventsModuleData> events, IdsCollector idsCollector ->
      events.stream()
          .filter({ e -> e.getOutcomeId() != null }).forEach({ e -> fillSiteServeData(e, eventName, outcomeName) })
    }

    when:
    def actualModules = moduleProcessor.getFirstFeaturedEventModules(sportModule, modularContent, Collections.emptySet())

    then:
    !actualModules.isEmpty()
  }

  def "Check featured module when first directive name is not featured"() {
    given:
    SportModule sportModule = createSportModule()
    ModularContent modularContent = getModularContent('featured_not_first_cms_modular_content_output.json')
    def outcomeName = 'Outcome name'
    def eventName = 'Event name'

    and:
    singleOutcomeDataInjector.injectData(*_) >> { List<EventsModuleData> events, IdsCollector idsCollector ->
      events.stream()
          .filter({ e -> e.getOutcomeId() != null }).forEach({ e -> fillSiteServeData(e, eventName, outcomeName) })
    }

    when:
    def actualModules = moduleProcessor.getFirstFeaturedEventModules(sportModule, modularContent, Collections.emptySet())

    then:
    !actualModules.isEmpty()
  }

  private ModularContent getModularContentMock() {
    return getModularContent('featured_consumption_cms_modular_content_output.json')
  }

  private ModularContent getModularContentEventHubMock() {
    return getModularContent('featured_eventhub_consumption_cms_modular_content_output.json')
  }

  private ModularContent getModularContent(String file) {
    List<ModularContentItem> items = getModularContentItemsFromResource(file)
    ModularContent modularContent = new ModularContent()
    modularContent.addAll(items)
    return modularContent
  }
}
