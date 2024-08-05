package com.oxygen.middleware.common.mappers

import com.coral.oxygen.middleware.common.mappers.FeaturedSimpleEventMapper
import com.coral.oxygen.middleware.common.mappers.MarketMapper
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.egalacoral.spark.siteserver.model.Children
import com.egalacoral.spark.siteserver.model.Event
import com.egalacoral.spark.siteserver.model.Market
import spock.lang.Specification

class FeaturedSimpleEventMapperSpec extends Specification {

  FeaturedSimpleEventMapper mapper

  MarketTemplateNameService marketTemplateNameService = Mock()
  MarketMapper marketMapper = Mock()

  def setup() {
    marketMapper.map(_, _) >> { arg1, arg2 ->
      def outputMarket = new OutputMarket()
      Market market = (Market) arg2
      outputMarket.setName(market.getName())
      outputMarket.setDisplayOrder(market.getDisplayOrder())
      return outputMarket
    }
    mapper = new FeaturedSimpleEventMapper(marketMapper, marketTemplateNameService)
  }

  def cleanup() {
    mapper = null
  }

  def "Test single market"() {
    given:
    def mappedEvent = new EventsModuleData()

    def market1 = new Market().tap {
      name = 'market1'
      displayOrder = 10
    }

    def market2 = new Market().tap {
      name = 'market2'
      displayOrder = 100
    }

    def market3 = new Market().tap {
      name = 'market3'
      displayOrder = 40
    }

    def child1 = new Children().tap {
      market = market1
    }

    def child2 = new Children().tap {
      market = market2
    }

    def child3 = new Children().tap {
      market = market3
    }

    def event = new Event().tap {
      id = '1'
      children = Arrays.asList(child3, child1, child2)
    }

    when:
    mapper.map(mappedEvent, event)

    then:
    1 == mappedEvent.getMarkets().size()
    3 == mappedEvent.getPrimaryMarkets().size()
    'market1' == mappedEvent.getMarkets().get(0).getName()
    10 == mappedEvent.getMarkets().get(0).getDisplayOrder()
  }

  def "Test single market1"() {
    given:
    def mappedEvent = new EventsModuleData()

    def market1 = new Market().tap {
      name = 'market1'
      displayOrder = 10
    }

    def market2 = new Market().tap {
      name = 'market2'
      displayOrder = 100
    }

    def market3 = new Market().tap {
      name = 'market3'
      displayOrder = 40
    }

    def child1 = new Children().tap {
      market = market1
    }

    def child2 = new Children().tap {
      market = market2
    }

    def child3 = new Children().tap {
      market = market3
      market.isMarketBetInRun = Boolean.TRUE
    }

    def event = new Event().tap {
      id = '1'
      isLiveNowEvent = Boolean.TRUE
      children = Arrays.asList(child3, child1, child2)
    }

    when:
    mapper.map(mappedEvent, event)

    then:
    1 == mappedEvent.getMarkets().size()
  }

  def "Test primary market with category"() {
    given:
    def mappedEvent = new EventsModuleData()

    marketTemplateNameService.getType(_) >> { String marketName ->
      if ('To reach the final' == marketName) {
        return MarketTemplateType.TO_REACH_THE_FINAL
      } else if ('Penalty Shoot-Out Winner' == marketName)
        return MarketTemplateType.PENALTY_SO_WINNER
      else if ('To Qualify' == marketName)
        return MarketTemplateType.TO_QUALIFY
      else
        return null
    }

    def market1 = new Market().tap {
      name = 'To reach the final'
      displayOrder = 10
    }

    def market2 = new Market().tap {
      name = 'Penalty Shoot-Out Winner'
      displayOrder = 100
    }

    def market3 = new Market().tap {
      name = 'To Qualify'
      displayOrder = 40
    }

    def child1 = new Children().tap {
      market = market1
    }

    def child2 = new Children().tap {
      market = market2
    }

    def child3 = new Children().tap {
      market = market3
    }

    def event = new Event().tap {
      id = '1'
      children = Arrays.asList(child3, child1, child2)
      categoryCode = 'FOOTBALL'
    }

    when:
    mapper.map(mappedEvent, event)

    then:
    1 == mappedEvent.getMarkets().size()
    3 == mappedEvent.getPrimaryMarkets().size()
    'Penalty Shoot-Out Winner' == mappedEvent.getMarkets().get(0).getName()
    100 == mappedEvent.getMarkets().get(0).getDisplayOrder()
  }

  def "Test single market first from the lowest Display Order"() {
    given:
    def mappedEvent = new EventsModuleData()

    def market1 = new Market().tap {
      name = 'market1'
      displayOrder = 10
    }

    def market2 = new Market().tap {
      name = 'market2'
      displayOrder = 100
    }

    def market3 = new Market().tap {
      name = 'market3'
      displayOrder = 10
    }

    def child1 = new Children().tap {
      market = market1
    }

    def child2 = new Children().tap {
      market = market2
    }

    def child3 = new Children().tap {
      market = market3
    }

    def event = new Event().tap {
      id = '1'
      children = Arrays.asList(child3, child1, child2)
    }

    when:
    mapper.map(mappedEvent, event)

    then:
    1 == mappedEvent.getMarkets().size()
    3 == mappedEvent.getPrimaryMarkets().size()
    'market3' == mappedEvent.getMarkets().get(0).getName()
    10 == mappedEvent.getMarkets().get(0).getDisplayOrder()
  }




  def "Test single market override true"() {
    given:
    def mappedEvent = new EventsModuleData()
    def market1 = new Market().tap {
      name = 'market1'
      displayOrder = 10
    }

    def market2 = new Market().tap {
      name = 'market2'
      displayOrder = 100
    }

    def market3 = new Market().tap {
      name = 'market3'
      displayOrder = 40
    }

    def child1 = new Children().tap {
      market = market1
    }

    def child2 = new Children().tap {
      market = market2
    }

    def child3 = new Children().tap {
      market = market3
    }

    def event = new Event().tap {
      id = '1'
      children = Arrays.asList(child3, child1, child2)
    }

    when:
    mapper.map(mappedEvent, event)

    then:
    1 == mappedEvent.getMarkets().size()
    3 == mappedEvent.getPrimaryMarkets().size()
    'market1' == mappedEvent.getMarkets().get(0).getName()
    10 == mappedEvent.getMarkets().get(0).getDisplayOrder()
  }
}
