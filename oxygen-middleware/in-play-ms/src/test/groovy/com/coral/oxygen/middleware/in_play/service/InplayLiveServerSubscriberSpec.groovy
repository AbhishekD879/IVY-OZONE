package com.coral.oxygen.middleware.in_play.service

import com.coral.oxygen.middleware.common.service.MarketTemplateNameService
import com.egalacoral.spark.liveserver.Subscriber
import com.egalacoral.spark.liveserver.service.LiveServerSubscriber
import com.egalacoral.spark.liveserver.service.LiveServerSubscriptionsQAStorage
import spock.lang.Specification

class InplayLiveServerSubscriberSpec extends Specification {
  InplayLiveServerSubscriber inplaySubscriber

  Subscriber liveServerClient
  LiveServerSubscriber liveServerSubscriber
  MarketTemplateNameService marketTemplateNameService
  LiveServerSubscriptionsQAStorage liveServerSubscriptionsQAStorage
  def setup() {
    liveServerClient = Mock(Subscriber)
    liveServerSubscriber = Mock(LiveServerSubscriber)
    marketTemplateNameService = Mock(MarketTemplateNameService)
    liveServerSubscriptionsQAStorage = Mock(LiveServerSubscriptionsQAStorage)
    marketTemplateNameService.getNames(*_) >> [
      "Match Betting",
      "Match Result",
      "First-Half Result",
      "Total Goals Over/Under 1.5",
      "Total Goals Over/Under 2.5",
      "Total Goals Over/Under 3.5",
      "Total Goals Over/Under 4.5",
      "To Qualify",
      "Draw No Bet",
      "Match Result and Both Teams To Score",
      "Both Teams to Score",
      "Penalty Shoot-Out Winner",
      "Penalty Shoot Out Winner",
      "Extra-Time Result",
      "Extra Time Result"
    ]
    marketTemplateNameService.containsName(*_) >> { type, name -> name != null && type.toString().replaceAll("_", "").equalsIgnoreCase(name.replaceAll("\\s", "")) }
    inplaySubscriber = new InplayLiveServerSubscriber(liveServerClient, liveServerSubscriptionsQAStorage, liveServerSubscriber, marketTemplateNameService, ["34"] as String[],[
      "Current Set Winner",
      "Current Game Winner"
    ] as String[])
  }

  def "InPlay should subscribe only to one Next Team To Score"() {
    when:
    inplaySubscriber.subscribe(TestTools.inPlayDataFromFile("InPlayDataSorterTest/nextTeamToScore.json").getLivenow())
    then:
    1 * liveServerSubscriber.subscribe(LiveServerSubscriber.EventSubscribeInfo.builder()
        .categoryId(16)
        .id("10")
        .market("111")
        .outcome("111111")
        .build());
  }

  def "Inplay should subscribe to current set winner"() {
    when:
    inplaySubscriber.subscribe(TestTools.inPlayDataFromFile("InPlayDataSorterTest/currentSetWinner.json").getLivenow())
    then:
    1 * liveServerSubscriber.subscribe(LiveServerSubscriber.EventSubscribeInfo.builder()
        .categoryId(34)
        .id("10")
        .market("111")
        .outcome("111111")
        .build());
  }

  def "Inplay should not subscribe to current set winner non live"() {
    when:
    inplaySubscriber.subscribe(TestTools.inPlayDataFromFile("InPlayDataSorterTest/currentSetWinnerNonLive.json").getLivenow())
    then:
    0 * liveServerSubscriber.subscribe(LiveServerSubscriber.EventSubscribeInfo.builder()
        .categoryId(34)
        .id("10")
        .market("111")
        .outcome("111111")
        .build());
  }
  def "Inplay should not subscribe if nonPrimaryMarketsForLiveUpdates is empty"() {

    inplaySubscriber = new InplayLiveServerSubscriber(liveServerClient, liveServerSubscriptionsQAStorage, liveServerSubscriber, marketTemplateNameService, ["34"] as String[],null)

    when:
    inplaySubscriber.subscribe(TestTools.inPlayDataFromFile("InPlayDataSorterTest/currentSetWinnerNonLive.json").getLivenow())
    then:
    0 * liveServerSubscriber.subscribe(LiveServerSubscriber.EventSubscribeInfo.builder()
        .categoryId(34)
        .id("10")
        .market("111")
        .outcome("111111")
        .build());
  }
  def "Inplay should not subscribe if nonPrimaryMarketsForLiveUpdates and sportsNeedSubForNonprimaryMarkets is empty"() {

    inplaySubscriber = new InplayLiveServerSubscriber(liveServerClient, liveServerSubscriptionsQAStorage, liveServerSubscriber, marketTemplateNameService, null,null)

    when:
    inplaySubscriber.subscribe(TestTools.inPlayDataFromFile("InPlayDataSorterTest/currentSetWinnerNonLive.json").getLivenow())
    then:
    0 * liveServerSubscriber.subscribe(LiveServerSubscriber.EventSubscribeInfo.builder()
        .categoryId(34)
        .id("10")
        .market("111")
        .outcome("111111")
        .build());
  }
  def "Inplay should subscribe only to Total OverUnder only up to 4.5 "() {
    when:
    inplaySubscriber.subscribe(TestTools.inPlayDataFromFile("InPlayDataSorterTest/overUnder.json").getLivenow())
    then:
    1 * liveServerSubscriber.subscribe(LiveServerSubscriber.EventSubscribeInfo.builder()
        .categoryId(16)
        .id("10")
        .market("111")
        .outcome("111111")
        .build());
  }

  def "Test methods calling on livenow events subscription"() {
    when:
    inplaySubscriber.subscribe(TestTools.inPlayDataFromFile("InPlayDataSorterTest/inputData.json").getLivenow())

    then:

    1 * liveServerSubscriber.subscribe(LiveServerSubscriber.EventSubscribeInfo.builder()
        .categoryId(16)
        .id("10")
        .market("1")
        .market("2")
        .market("456")
        .outcome("2")
        .outcome("3")
        .outcome("4")
        .outcome("654")
        .build());

    1 * liveServerSubscriber.subscribe(LiveServerSubscriber.EventSubscribeInfo.builder()
        .categoryId(16)
        .id("20")
        .market("1")
        .market("2")
        .outcome("2")
        .build())

    1 * liveServerSubscriber.subscribe(LiveServerSubscriber.EventSubscribeInfo.builder()
        .categoryId(16)
        .id("1")
        .market("1")
        .market("2")
        .market("3")
        .market("4")
        .market("5")
        .market("6")
        .market("7")
        .market("8")
        .market("9")
        .market("10")
        .market("11")
        .market("12")
        .market("13")
        .market("14")
        .outcome("1")
        .outcome("2")
        .outcome("3")
        .outcome("4")
        .outcome("5")
        .outcome("6")
        .outcome("7")
        .outcome("8")
        .outcome("9")
        .outcome("10")
        .outcome("11")
        .outcome("12")
        .outcome("13")
        .outcome("14")
        .build())

    1 * liveServerSubscriber.subscribe(LiveServerSubscriber.EventSubscribeInfo.builder()
        .categoryId(16)
        .id("2")
        .build())

    1 * liveServerSubscriber.subscribe(LiveServerSubscriber.EventSubscribeInfo.builder()
        .categoryId(16)
        .id("3")
        .market("3")
        .build())
  }
}
