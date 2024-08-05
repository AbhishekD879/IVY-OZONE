package com.coral.oxygen.middleware.common.utils

import com.coral.oxygen.middleware.common.service.MarketTemplateNameService
import com.egalacoral.spark.siteserver.api.ExistsFilter
import com.egalacoral.spark.siteserver.api.LimitRecordsFilter
import com.egalacoral.spark.siteserver.api.LimitToFilter
import com.egalacoral.spark.siteserver.api.SimpleFilter
import org.springframework.test.util.ReflectionTestUtils
import spock.lang.Specification

import java.time.Duration

class QueryFilterBuilderSpec extends Specification {

  QueryFilterBuilder queryFilterBuilder
  MarketTemplateNameService marketTemplateNameService = Mock()

  def setup() {
    queryFilterBuilder = new QueryFilterBuilder(marketTemplateNameService)
    ReflectionTestUtils.setField(queryFilterBuilder, "iHRMaxMinutes", "30");
  }

  def "Construct class simple filter"() {
    when:
    SimpleFilter simpleFilter = queryFilterBuilder.getClassSimpleFilter("15,16")

    then:
    3 == simpleFilter.getQueryMap().size()
    "class.isActive" == simpleFilter.getQueryMap().get(0)
    "class.categoryId:intersects:15,16" == simpleFilter.getQueryMap().get(1)
    "class.siteChannels:contains:M" == simpleFilter.getQueryMap().get(2)
  }

  def "Construct class simple filter for virtual"() {
    when:
    SimpleFilter simpleFilter = queryFilterBuilder.getFilterForVirtualEvents()

    then:
    6 == simpleFilter.getQueryMap().size()
    "event.isStarted:isFalse" == simpleFilter.getQueryMap().get(0)
    "event.isLiveNowEvent:isFalse" == simpleFilter.getQueryMap().get(1)
  }


  def "Construct class existing filter"() {
    when:
    ExistsFilter filter = queryFilterBuilder.getClassExistingFilter()

    then:
    2 == filter.getQueryMap().size()
    "class:simpleFilter:event.siteChannels:contains:M" == filter.getQueryMap().get(0)
    "class:simpleFilter:event.drilldownTagNames:intersects:EVFLAG_BL" == filter.getQueryMap().get(1)
  }

  def "Construct event to outcome for class existing filter nor HHAndMR"() {
    when:
    ExistsFilter filter = queryFilterBuilder.getEventToOutcomeForClassExistingFilter(true)
    queryFilterBuilder.getEventToOutcomeForClassExistingFilter(false)
    then:
    4 == filter.getQueryMap().size()
    filter.getQueryMap().contains("market:simpleFilter:outcome.outcomeMeaningMajorCode:in:HH,MR,H1")
  }

  def "Construct event to outcome for class existingFilter"() {
    when:
    ExistsFilter filter = queryFilterBuilder.getEventToOutcomeForClassExistingFilter(true)

    then:
    4 == filter.getQueryMap().size()
    "market:simpleFilter:outcome.outcomeMeaningMajorCode:in:HH,MR,H1" == filter.getQueryMap().get(0)
  }

  def "Construct event to outcome for class limit filter"() {
    when:
    LimitToFilter filter = queryFilterBuilder.getLowestMarketDisplayOrderLimitFilter()

    then:
    1 == filter.getQueryMap().size()
    "market.displayOrder:isLowest" == filter.getQueryMap().get(0)
  }

  def "Construct event to outcome for class filter excluding Outright"() {
    when:
    SimpleFilter filter = queryFilterBuilder.getEventToOutcomeForClassFilterExcludeTemplate("|Outright|")

    then:
    9 == filter.getQueryMap().size()
    "market.isMarketBetInRun" == filter.getQueryMap().get(0)
    "event.siteChannels:contains:M" == filter.getQueryMap().get(1)
    "market.siteChannels:contains:M" == filter.getQueryMap().get(2)
    "outcome.siteChannels:contains:M" == filter.getQueryMap().get(3)
    "event.drilldownTagNames:intersects:EVFLAG_BL" == filter.getQueryMap().get(4)
    "market.templateMarketName:notIntersects:|Outright|" == filter.getQueryMap().get(8)
    filter.getQueryMap().get(5).endsWith("0.000")
  }

  def "Construct event to outcome with outright markets"() {
    when:
    SimpleFilter filter = queryFilterBuilder.getEventToOutcomeForClassFilterWithMarketTemlates("|Outright|")

    then:
    9 == filter.getQueryMap().size()
    "market.isMarketBetInRun" == filter.getQueryMap().get(0)
    "event.siteChannels:contains:M" == filter.getQueryMap().get(1)
    "market.siteChannels:contains:M" == filter.getQueryMap().get(2)
    "outcome.siteChannels:contains:M" == filter.getQueryMap().get(3)
    "event.drilldownTagNames:intersects:EVFLAG_BL" == filter.getQueryMap().get(4)
    "market.templateMarketName:intersects:|Outright|" == filter.getQueryMap().get(8)
    filter.getQueryMap().get(5).endsWith("0.000")
  }

  def "Construct live market count event for class simple filter"() {
    when:
    SimpleFilter filter = queryFilterBuilder.getMarketCountForLiveOrUpcomingEventSimpleFilter()

    then:
    7 == filter.getQueryMap().size()
    "event.typeName:notEquals:|Enhanced Multiples|" == filter.getQueryMap().get(0)
    "event.siteChannels:contains:M" == filter.getQueryMap().get(1)
    "market.siteChannels:contains:M" == filter.getQueryMap().get(2)
    "event.drilldownTagNames:intersects:EVFLAG_BL" == filter.getQueryMap().get(3)
  }

  def "Construct getLiveOrUpcomingEventToOutcomeByHRPrimMarket"() {
    when:
    Duration startTime = Duration.ofDays(1)
    String marketData = "market.name:in:|Win or Each Way|,|To Win|,|To-Win|,|Win/EachWay|,|Win or each way|,|Meeting Winner|,|Win Only|,Win or Each Way,To Win,To-Win,Win/EachWay,Win or each way,Meeting Winner,Win Only"
    SimpleFilter filter = queryFilterBuilder.getLiveOrUpcomingEventToOutcomeByHRPrimMarket(marketData)
    QueryFilterBuilder.getClassWithOpenEventsSimpleFilter("223")
    QueryFilterBuilder.getEmptyExistingFilter()
    queryFilterBuilder.getEventToOutcomeForAllActiveMarkets()
    QueryFilterBuilder.getNotSpecialEventsExistFilter()
    queryFilterBuilder.getLiveOrUpcomingEventToOutcomeByPrimMarket(marketData)
    QueryFilterBuilder.getEmptyLimitFilter()
    QueryFilterBuilder.getEmptyLimitRecordsFilter()
    QueryFilterBuilder.getMarketOutcomesLimitRecordsFilter(3,6)
    queryFilterBuilder.getHRMarketCountForLiveOrUpcomingEventSimpleFilter()
    QueryFilterBuilder.getRacingEventByTypeFlagsWithStartTimeUntil("HH","DF",startTime,"GETS")
    QueryFilterBuilder.getToteEventBySelectionTimeRange(startTime)
    queryFilterBuilder.getFilterForOutrightEvents()
    queryFilterBuilder.getFilterForNotStartedEvents()
    queryFilterBuilder.getFilterForFootballEvents()
    queryFilterBuilder.getFilterForFootballEvents("2UpMarket")
    queryFilterBuilder.getFilterForNonFootballEvents()
    queryFilterBuilder.getLiveFootballEventToOutcomeForClassFilter()
    QueryFilterBuilder.getNextRaces("23")
    QueryFilterBuilder.getPoolTypesPredicate(Arrays.asList("HH","RF"))


    then:
    9 == filter.getQueryMap().size()
    "market.isMarketBetInRun" == filter.getQueryMap().get(0)
  }
  def "Construct filter for virtuals"(){

    when:
    ExistsFilter existsFilter = QueryFilterBuilder.getClassExistingFilterVirtuaHub()
    then:
    existsFilter.getQueryMap().size() == 1
    existsFilter.getQueryMap().get(0).contains("class:simpleFilter:event.siteChannels:contains:M")
  }

  def "get Active Classes For TheCategory" () {
    when:
    SimpleFilter simpleFilter = queryFilterBuilder.getActiveClassesForTheCategory("223,456")
    then:
    simpleFilter!=null
    simpleFilter.getQueryMap().size() ==4
  }

  def "build simple filter for next races" () {
    when:
    SimpleFilter simpleFilter = queryFilterBuilder.buildSimpleFilterForNextRaces("UK")
    then:
    simpleFilter!=null
    simpleFilter.getQueryMap().size() ==12
  }

  def "build exists filter for next races" () {
    when:
    ExistsFilter existsFilter = queryFilterBuilder.buildExistsFilterForNextRaces()
    then:
    existsFilter!=null
    existsFilter.getQueryMap().size()==1
  }

  def "build limit records filter for next races" () {

    when:
    LimitRecordsFilter filter = queryFilterBuilder.buildLimitRecordsFilterForNextRaces()
    then:
    filter!=null
    filter.getQueryMap().size()==1
  }
}
