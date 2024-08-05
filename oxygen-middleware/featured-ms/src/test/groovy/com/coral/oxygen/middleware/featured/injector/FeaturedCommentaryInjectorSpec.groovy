package com.coral.oxygen.middleware.featured.injector

import com.coral.oxygen.cms.api.SystemConfigProvider
import com.coral.oxygen.middleware.common.service.featured.IdsCollector
import com.coral.oxygen.middleware.featured.service.injector.FeaturedCommentaryInjector
import com.coral.oxygen.middleware.featured.service.injector.FeaturedSiteServerService
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModel
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.coral.oxygen.middleware.pojos.model.output.featured.EventsModule
import com.egalacoral.spark.siteserver.model.Children
import com.egalacoral.spark.siteserver.model.Event
import spock.lang.Specification

import java.util.function.Function
import java.util.stream.Collectors

import static com.coral.oxygen.middleware.featured.utils.FeaturedDataUtils.getSSEventCommentaryForEvent
import static com.coral.oxygen.middleware.featured.utils.FeaturedDataUtils.getSSEventsFromResource

class FeaturedCommentaryInjectorSpec extends Specification {
  FeaturedCommentaryInjector commentaryInjector

  FeaturedSiteServerService siteServerService
  IdsCollector idsCollector
  SystemConfigProvider systemConfigProvider
  CmsSystemConfig cmsSystemConfig

  def setup() {
    siteServerService = Mock()
    idsCollector = Mock(IdsCollector)
    systemConfigProvider = Mock(SystemConfigProvider)
    cmsSystemConfig = Mock(CmsSystemConfig)

    List<Event> eventsWithComments =
        extractPureEventsFromChildren(getSSEventsFromResource("injector_comments_content.json"))
    siteServerService.getCommentaryForEvent(_ as List) >> eventsWithComments.stream().collect(Collectors.toMap({e -> e.getId()}, Function.identity()))

    commentaryInjector = new FeaturedCommentaryInjector(siteServerService, systemConfigProvider)
  }

  def "Injecting data with comments and facts passing good"() {
    List<Children> childrensWithEvents = getSSEventCommentaryForEvent("injector_events_without_comments.json")
    List<Event> pureEvents = extractPureEventsFromChildren(childrensWithEvents)
    List<EventsModuleData> moduleDataItemList = pureEvents.stream().map({ event ->
      EventsModuleData moduleDataItem = new EventsModuleData()
      moduleDataItem.setId(Long.valueOf(event.getId()))
      moduleDataItem.setMarkets(Arrays.asList(marketToOutputMarket(event)))
      moduleDataItem.setCategoryCode(event.getCategoryCode())
      return moduleDataItem
    }).collect(Collectors.toList())

    EventsModule outputModule = new EventsModule()
    outputModule.setData(moduleDataItemList)
    FeaturedModel result = new FeaturedModel()
    result.setModules(Arrays.asList(outputModule))

    when:
    commentaryInjector.injectData(moduleDataItemList, idsCollector)
    EventsModuleData firstEvent = result.getModules().get(0).getData().get(0)
    EventsModuleData secondEvent = result.getModules().get(0).getData().get(1)
    EventsModuleData thirdEvent = result.getModules().get(0).getData().get(2)
    Map fact = (Map) ((Map) secondEvent.getComments().getFacts().get(1)).get("eventFact")

    then:
    systemConfigProvider.systemConfig() >> cmsSystemConfig
    cmsSystemConfig.getBipScoreEvents() >> new HashMap<String, Boolean>()
    null == firstEvent.getComments()
    "196992" == fact.get("id")
    "5433366" == fact.get("eventId")
    "23422" == fact.get("eventParticipantId")
    "103921" == fact.get("eventPeriodId")
    "1" == fact.get("fact")
    "SCORE" == fact.get("factCode")
    "Score of the match/game" == fact.get("name")
    null == thirdEvent.getComments()
  }

  private List<Event> extractPureEventsFromChildren(List<Children> childrensWithEvents) {
    return childrensWithEvents.stream()
        .filter({ child -> child.getEvent() != null })
        .map({child -> child.getEvent()})
        .collect(Collectors.toList())
  }

  private OutputMarket marketToOutputMarket(Event event) {
    OutputMarket outputMarket = new OutputMarket()
    outputMarket.setId(event.getMarkets().get(0).getId())
    outputMarket.setMarketBetInRun(true)
    return outputMarket
  }
}
