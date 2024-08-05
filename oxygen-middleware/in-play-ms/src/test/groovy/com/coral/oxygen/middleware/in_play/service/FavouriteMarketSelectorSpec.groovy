package com.coral.oxygen.middleware.in_play.service;

import com.coral.oxygen.middleware.in_play.service.market.selector.FavouriteMarketSelector
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment

import spock.lang.Specification

public class FavouriteMarketSelectorSpec extends Specification{

  FavouriteMarketSelector favouriteMarketSelector
  String[] marketNamesToKeep
  SportSegment sportSegment

  def setup() {
    sportSegment = TestTools.fromFile("MarketSelectorServiceTest/events4.json", SportSegment.class)
    marketNamesToKeep = ["Total Points"] as String[]
    favouriteMarketSelector = new FavouriteMarketSelector(marketNamesToKeep, TestTools.GSON)
  }

  def "Test splitting sport segment - BasketballLiveEvent_EmptyRawHandicap"() {
    String[] prorityMarket
    when:
    EventsModuleData event =sportSegment.getEventsByTypeName().get(0).getEvents().get(0)
    prorityMarket = favouriteMarketSelector.getPriorityMarket(event);
    then:
    // Changed assertion from content comparison to length and number of segment splits to overcome edit distance issue
    null == prorityMarket[0]
    null == prorityMarket[1]
  }

  def "Test splitting sport segment - BasketballLiveEvent_EmptyMarketName"() {
    String[] prorityMarket
    Boolean isPriorityMarket
    when:
    prorityMarket = ["Total Points", "7.5"]
    OutputMarket market =sportSegment.getEventsByTypeName().get(0).getEvents().get(0).getMarkets().get(0);
    market.setTemplateMarketName(null)
    isPriorityMarket = favouriteMarketSelector.priorityMarket(market,prorityMarket);
    then:
    // Changed assertion from content comparison to length and number of segment splits to overcome edit distance issue
    isPriorityMarket == false
  }

  def "Test splitting sport segment - BasketballLiveEvent_DiffMarketName"() {
    String[] prorityMarket
    Boolean isPriorityMarket
    when:
    prorityMarket = ["Handicap", "7.5"]
    OutputMarket market =sportSegment.getEventsByTypeName().get(0).getEvents().get(0).getMarkets().get(0);
    market.setTemplateMarketName("Total Points")
    isPriorityMarket = favouriteMarketSelector.priorityMarket(market,prorityMarket);
    then:
    // Changed assertion from content comparison to length and number of segment splits to overcome edit distance issue
    isPriorityMarket == false
  }

  def "Test splitting sport segment - BasketballLiveEvent_EmptyRawHandicap2"() {
    String[] prorityMarket
    when:
    EventsModuleData event =sportSegment.getEventsByTypeName().get(0).getEvents().get(0)
    event.getMarkets().get(0).setRawHandicapValue(null)
    event.getMarkets().get(0).setName("Total Points")
    prorityMarket = favouriteMarketSelector.getPriorityMarket(event);
    then:
    "Money Line" == prorityMarket[0]
    null == prorityMarket[1]
  }


  def cleanup() {
    favouriteMarketSelector = null
  }
}
