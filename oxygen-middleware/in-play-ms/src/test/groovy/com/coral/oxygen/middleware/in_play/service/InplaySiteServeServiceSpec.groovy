package com.coral.oxygen.middleware.in_play.service

import com.coral.oxygen.middleware.common.service.MarketTemplateNameService
import com.coral.oxygen.middleware.common.utils.QueryFilterBuilder
import com.coral.oxygen.middleware.in_play.service.siteserver.InplaySiteServeService
import com.coral.oxygen.middleware.pojos.model.output.PrimaryMarkets
import com.egalacoral.spark.siteserver.api.BinaryOperation
import com.egalacoral.spark.siteserver.api.ExistsFilter
import com.egalacoral.spark.siteserver.api.LimitToFilter
import com.egalacoral.spark.siteserver.api.SimpleFilter
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.api.UnaryOperation
import com.egalacoral.spark.siteserver.model.Aggregation
import com.egalacoral.spark.siteserver.model.Category
import com.egalacoral.spark.siteserver.model.Event
import org.springframework.test.util.ReflectionTestUtils
import spock.lang.Ignore
import spock.lang.Specification

class InplaySiteServeServiceSpec extends Specification {

  SiteServerApi siteServerApi = Mock()
  MarketTemplateNameService marketTemplateNameService = Mock()
  OutrightOutcomesFilter topThreeOutrightOutcomesFilter = Mock()
  QueryFilterBuilder queryFilterBuilder
  InplaySiteServeService inplaySiteServeService
  SimpleFilter simpleFilter = Mock()

  def setup() {
    queryFilterBuilder = new QueryFilterBuilder(marketTemplateNameService)
    ReflectionTestUtils.setField(queryFilterBuilder, "iHRMaxMinutes", "30")
    inplaySiteServeService = new InplaySiteServeService(siteServerApi, marketTemplateNameService, topThreeOutrightOutcomesFilter,queryFilterBuilder);
  }

  def "Get Classes By CategoryIds"(){
    Category[] categories1 = TestTools.fromFile("InPlayDataConsumerTest/classes1.json", Category[].class)
    Category[] categories2 = TestTools.fromFile("InPlayDataConsumerTest/classes2.json", Category[].class)

    given:
    siteServerApi.getClasses(*_) >>>
        [
          Optional.of(Arrays.asList(categories1)),
          Optional.of(Arrays.asList(categories2))
        ]
    when:
    Set<String> categoryIds = new HashSet<>()
    categoryIds.add("21")
    categoryIds.add("16")
    List<Category> categories =  inplaySiteServeService.getClasses(categoryIds)

    then:
    categories.size() == 5
  }

  def "Get Live BasketBall Events" () {
    List<Event> expectedEvents
    Event[] outrightsExcludedEventsBasketball = new ArrayList<>();
    Event[] eventsWithPrimaryMarketsBasketball = TestTools.fromFile("MarketSelectorServiceTest/eventsWithPrimaryMarketsBasketball.json", Event[].class)
    Event[] liveEventsBasketball = TestTools.fromFile("MarketSelectorServiceTest/liveEventsBasketball.json", Event[].class)

    given:
    siteServerApi.getEventToOutcomeForClass(Arrays.asList("75", "97", "108", "166", "97", "108", "105"),
        _ as SimpleFilter,
        _ as LimitToFilter,
        _ as ExistsFilter) >>
        Optional.of(Arrays.asList(liveEventsBasketball))

    siteServerApi.getEventToOutcomeForClass(Arrays.asList("75", "97", "108", "166", "97", "108", "105"),
        _ as SimpleFilter,
        _ as LimitToFilter,
        _ as ExistsFilter,
        Collections.singletonList("event")) >>
        Optional.of(Arrays.asList(eventsWithPrimaryMarketsBasketball))

    topThreeOutrightOutcomesFilter.filterOutcomes(_) >> Arrays.asList(outrightsExcludedEventsBasketball);

    PrimaryMarkets primaryMarketCategory = PrimaryMarkets.BASKETBALL;
    List<String> classIds= Arrays.asList("75", "97", "108", "166", "97", "108", "105")

    when:
    expectedEvents = inplaySiteServeService.getEvents(primaryMarketCategory, classIds);
    then:
    5 == expectedEvents.size();
  }

  def "Get Live BasketBall Events NullPrimaryMarket" () {
    List<Event> expectedEvents
    Event[] outrightsExcludedEventsBasketball = new ArrayList<>();
    Event[] eventsWithPrimaryMarketsBasketball = TestTools.fromFile("MarketSelectorServiceTest/eventsWithPrimaryMarketsBasketball.json", Event[].class)
    Event[] liveEventsBasketball = TestTools.fromFile("MarketSelectorServiceTest/liveEventsBasketball.json", Event[].class)

    given:
    siteServerApi.getEventToOutcomeForClass(Arrays.asList("75", "97", "108", "166", "97", "108", "105"),
        _ as SimpleFilter,
        _ as LimitToFilter,
        _ as ExistsFilter) >>
        Optional.of(Arrays.asList(liveEventsBasketball))

    siteServerApi.getEventToOutcomeForClass(Arrays.asList("75", "97", "108", "166", "97", "108", "105"),
        _ as SimpleFilter,
        _ as LimitToFilter,
        _ as ExistsFilter,
        Collections.singletonList("event")) >>
        Optional.of(Arrays.asList(eventsWithPrimaryMarketsBasketball))

    topThreeOutrightOutcomesFilter.filterOutcomes(_) >> Arrays.asList(outrightsExcludedEventsBasketball);

    PrimaryMarkets primaryMarketCategory = null;
    List<String> classIds= Arrays.asList("75", "97", "108", "166", "97", "108", "105")

    when:
    expectedEvents = inplaySiteServeService.getEvents(primaryMarketCategory, classIds);
    then:
    4 == expectedEvents.size();
  }

  def "Get Live BasketBall Events With different PrimaryMarket" () {
    List<Event> expectedEvents
    Event[] outrightsExcludedEventsBasketball = new ArrayList<>();
    Event[] eventsWithPrimaryMarketsBasketball = TestTools.fromFile("MarketSelectorServiceTest/eventsWithPrimaryMarketsBasketball.json", Event[].class)
    Event[] liveEventsBasketball = TestTools.fromFile("MarketSelectorServiceTest/liveEventsBasketball.json", Event[].class)

    given:
    siteServerApi.getEventToOutcomeForClass(Arrays.asList("75", "97", "108", "166", "97", "108", "105"),
        _ as SimpleFilter,
        _ as LimitToFilter,
        _ as ExistsFilter) >>
        Optional.of(Arrays.asList(liveEventsBasketball))

    siteServerApi.getEventToOutcomeForClass(Arrays.asList("75", "97", "108", "166", "97", "108", "105"),
        _ as SimpleFilter,
        _ as LimitToFilter,
        _ as ExistsFilter,
        Collections.singletonList("event")) >>
        Optional.of(Arrays.asList(eventsWithPrimaryMarketsBasketball))

    topThreeOutrightOutcomesFilter.filterOutcomes(_) >> Arrays.asList(outrightsExcludedEventsBasketball);

    PrimaryMarkets primaryMarketCategory = PrimaryMarkets.NON_FOOTBALL;
    List<String> classIds= Arrays.asList("75", "97", "108", "166", "97", "108", "105")

    when:
    expectedEvents = inplaySiteServeService.getEvents(primaryMarketCategory, classIds);
    then:
    4 == expectedEvents.size();
  }

  def "Get Live BasketBall Events With HR PrimaryMarket" () {
    List<Event> expectedEvents
    Event[] outrightsExcludedEventsBasketball = new ArrayList<>();
    Event[] eventsWithPrimaryMarketsBasketball = TestTools.fromFile("MarketSelectorServiceTest/eventsWithPrimaryMarketsBasketball.json", Event[].class)
    Event[] liveEventsBasketball = TestTools.fromFile("MarketSelectorServiceTest/liveEventsBasketball.json", Event[].class)

    given:
    siteServerApi.getEventToOutcomeForClass(Arrays.asList("75", "97", "108", "166", "97", "108", "105"),
        _ as SimpleFilter,
        _ as LimitToFilter,
        _ as ExistsFilter) >>
        Optional.of(Arrays.asList(liveEventsBasketball))

    siteServerApi.getEventToOutcomeForClass(Arrays.asList("75", "97", "108", "166", "97", "108", "105"),
        _ as SimpleFilter,
        _ as LimitToFilter,
        _ as ExistsFilter,
        Collections.singletonList("event")) >>
        Optional.of(Arrays.asList(eventsWithPrimaryMarketsBasketball))

    topThreeOutrightOutcomesFilter.filterOutcomes(_) >> Arrays.asList(outrightsExcludedEventsBasketball);

    PrimaryMarkets primaryMarketCategory = PrimaryMarkets.HORSE_RACING;
    List<String> classIds= Arrays.asList("75", "97", "108", "166", "97", "108", "105")

    queryFilterBuilder.getLiveOrUpcomingEventToOutcomeByHRPrimMarket(
        marketTemplateNameService.asQuery(primaryMarketCategory.getPrimaryMarkets())) >> simpleFilter

    when:
    expectedEvents = inplaySiteServeService.getEvents(primaryMarketCategory, classIds);
    then:
    4 == expectedEvents.size();
  }

  def "Get HR MarketCount per Event"(){

    given:
    Aggregation[] aggregation1 = TestTools.fromFile("InPlayDataConsumerTest/marketsCount1.json", Aggregation[].class)

    siteServerApi.getEventMarketsCountForClass(Arrays.asList("97", "108", "105"), _) >>
        Optional.of(Arrays.asList(aggregation1))

    when:
    Set<String> categoryIds = new HashSet<>()
    categoryIds.add("21")
    categoryIds.add("16")
    Map<String, Integer> hrcounts =  inplaySiteServeService.getHRMarketsCountPerEventForClass(Arrays.asList("97", "108", "105"))

    then:
    hrcounts.size() == 6
  }

  def "Get Non HR MarketCount per Event"(){

    given:
    Aggregation[] aggregation1 = TestTools.fromFile("InPlayDataConsumerTest/marketsCount1.json", Aggregation[].class)

    siteServerApi.getEventMarketsCountForClass(Arrays.asList("97", "108", "105"), _) >>
        Optional.of(Arrays.asList(aggregation1))

    when:
    Set<String> categoryIds = new HashSet<>()
    categoryIds.add("21")
    categoryIds.add("16")
    Map<String, Integer> hrcounts =  inplaySiteServeService.getMarketsCountPerEventForClass(Arrays.asList("97", "108", "105"))

    then:
    hrcounts.size() == 6
  }
  def "get virtual events"() {
    given:
    Event[] virtualEvents = TestTools.fromFile("InPlayDataConsumerTest/virtualEvents.json", Event[].class)
    Category[] virtualCategories = TestTools.fromFile("InPlayDataConsumerTest/virtualCategories.json", Category[].class)

    //        inplaySiteServeService.getClassesforVirtualHub() >> Arrays.asList(virtualCategories)

    siteServerApi.getEventToOutcomeForClass(Arrays.asList("75", "97", "108", "166", "97", "108", "105"),
        _ as SimpleFilter,
        _ as LimitToFilter,
        _ as ExistsFilter)  >> Optional.of(Arrays.asList(virtualEvents))

    siteServerApi.getClasses(_ as SimpleFilter, _ as ExistsFilter) >> Optional.of(Arrays.asList(virtualCategories))
    List<Event> eventList
    List<Category> categoryList
    when:
    eventList =  inplaySiteServeService.getVirtualEvents(Arrays.asList("75", "97", "108", "166", "97", "108", "105"))
    categoryList = inplaySiteServeService.getClassesforVirtualHub()
    then:
    !eventList.isEmpty()
    !categoryList.isEmpty()

  }
}
