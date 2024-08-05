package com.oxygen.publisher.inplay.service

import com.oxygen.publisher.model.Comment
import com.oxygen.publisher.model.InPlayByEventMarket
import com.oxygen.publisher.model.ModuleDataItem
import com.oxygen.publisher.model.OutputMarket
import com.oxygen.publisher.model.RawIndex
import spock.lang.Specification

class AbstractInPlayChainFactorySpec extends Specification {

  def "Create PR Market Cache Index"() {
    setup:
    def market = new OutputMarket()
    market.id = "2"

    expect:
    "1::2" == AbstractInPlayChainFactory.createPRMarketCacheIndex(1, Collections.singletonList(market))
    "1::" == AbstractInPlayChainFactory.createPRMarketCacheIndex(1, null)
    "1::" == AbstractInPlayChainFactory.createPRMarketCacheIndex(1, new ArrayList<>())
  }

  def "Event is updates even if cached in PR markets cache"() {
    when:
    def inPlayByEventMarket = new InPlayByEventMarket()
    def cachedItem = createModuleItem()
    cachedItem.eventIsLive = false
    inPlayByEventMarket.setModuleDataItem(cachedItem)
    def prMarketCache = ["123::321": inPlayByEventMarket]
    ModuleDataItem item = createModuleItem()
    item.eventIsLive = true
    def events = AbstractInPlayChainFactory.optimizeEvents(prMarketCache, [item], RawIndex.builder()
    .categoryId(16)
    .typeId(111)
    .topLevelType("LIVE_EVENT")
    .build())
    then:
    events[0].eventIsLive
  }

  private ModuleDataItem createModuleItem() {
    def item = new ModuleDataItem()
    item.id = 123
    def market = new OutputMarket()
    market.id = "321"
    item.setMarkets([market])
    item.setPrimaryMarkets([market])
    item
  }

  def "check market ordering"() {
    given:
    RawIndex rawIndex = RawIndex.builder().categoryId(16).typeId(442)
        .marketSelector("Next Team to Score").build()
    and:
    ModuleDataItem event = new ModuleDataItem()
    event.setMarketsCount(2)
    List<OutputMarket> markets = new ArrayList<>()
    OutputMarket market1 = new OutputMarket()
    market1.setName("Market_1")
    market1.setDisplayOrder(dispOrderMarket1)
    OutputMarket market2 = new OutputMarket()
    market2.setName("Market_2")
    market2.setDisplayOrder(dispOrderMarket2)

    markets.add(market1)
    markets.add(market2)
    event.setMarkets(markets)

    and:
    AbstractInPlayChainFactory.cropMarkets(rawIndex, event)

    expect:
    event.getMarkets().get(0).getName().equalsIgnoreCase(validMarketName)

    where:
    dispOrderMarket1 | dispOrderMarket2 | validMarketName
    -500             | 0                | "Market_1"
    -450             | -475             | "Market_2"
  }

  def "check market ordering case2"() {
    given:
    RawIndex rawIndex = RawIndex.builder().categoryId(34).typeId(442)
        .marketSelector("Current Set Winner").build()
    and:
    ModuleDataItem event = new ModuleDataItem()
    event.setCategoryId("34")
    event.setMarketsCount(2)
    Comment comment = new Comment()
    comment.setRunningSetIndex(1)
    event.setComments(comment)
    List<OutputMarket> markets = new ArrayList<>()
    OutputMarket market1 = new OutputMarket()
    market1.setName("Market_1")
    market1.setDisplayOrder(dispOrderMarket1)
    OutputMarket market2 = new OutputMarket()
    market2.setName("Market_2")
    market2.setDisplayOrder(dispOrderMarket2)

    markets.add(market1)
    markets.add(market2)
    event.setMarkets(markets)

    and:
    AbstractInPlayChainFactory.cropMarkets(rawIndex, event)

    expect:
    event.getMarkets().get(0).getName().equalsIgnoreCase(validMarketName)

    where:
    dispOrderMarket1 | dispOrderMarket2 | validMarketName
    -500             | 0                | "Market_1"
  }

  def "check market ordering case3"() {
    given:
    RawIndex rawIndex = RawIndex.builder().categoryId(34).typeId(442)
        .marketSelector("Current Game Winner").build()
    and:
    ModuleDataItem event = new ModuleDataItem()
    event.setCategoryId("34")
    event.setMarketsCount(2)
    Comment comment = new Comment()
    comment.setRunningSetIndex(1)
    event.setComments(comment)
    List<OutputMarket> markets = new ArrayList<>()
    OutputMarket market1 = new OutputMarket()
    market1.setName("Market_1")
    market1.setDisplayOrder(dispOrderMarket1)
    OutputMarket market2 = new OutputMarket()
    market2.setName("Market_2")
    market2.setDisplayOrder(dispOrderMarket2)

    markets.add(market1)
    markets.add(market2)
    event.setMarkets(markets)

    and:
    AbstractInPlayChainFactory.cropMarkets(rawIndex, event)

    expect:
    event.getMarkets().get(0).getName().equalsIgnoreCase(validMarketName)

    where:
    dispOrderMarket1 | dispOrderMarket2 | validMarketName
    -500             | 0                | "Market_1"
  }

  def "check market ordering case4"() {
    given:
    RawIndex rawIndex = RawIndex.builder().categoryId(34).typeId(442)
        .marketSelector("Current Set Winner").build()
    and:
    ModuleDataItem event = new ModuleDataItem()
    event.setCategoryId("34")
    event.setMarketsCount(2)
    List<OutputMarket> markets = new ArrayList<>()
    OutputMarket market1 = new OutputMarket()
    market1.setName("Market_1")
    market1.setDisplayOrder(dispOrderMarket1)
    OutputMarket market2 = new OutputMarket()
    market2.setName("Market_2")
    market2.setDisplayOrder(dispOrderMarket2)

    markets.add(market1)
    markets.add(market2)
    event.setMarkets(markets)

    and:
    AbstractInPlayChainFactory.cropMarkets(rawIndex, event)

    expect:
    event.getMarkets().get(0).getName().equalsIgnoreCase(validMarketName)

    where:
    dispOrderMarket1 | dispOrderMarket2 | validMarketName
    -500             | 0                | "Market_1"
  }
}
