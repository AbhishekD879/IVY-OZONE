package com.oxygen.middleware.common.mappers

import com.coral.oxygen.middleware.common.mappers.MarketHandicapTypeMapper
import com.coral.oxygen.middleware.common.mappers.MarketMapper
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.egalacoral.spark.siteserver.model.Event
import com.egalacoral.spark.siteserver.model.Market
import spock.lang.Specification

class MarketHandicapTypeMapperSpec extends Specification {

  MarketTemplateNameService marketTemplateNameService = Mock()
  MarketHandicapTypeMapper mapper

  MarketMapper chain = Mock()

  def setup() {
    chain.map(_, _) >> new OutputMarket()
    mapper = new MarketHandicapTypeMapper(chain, marketTemplateNameService)

    marketTemplateNameService.containsName(_, _) >> { templateType, marketName ->
      def expectedTemplateName = templateType.toString().replaceAll('_', ' ')
      return expectedTemplateName.equalsIgnoreCase(marketName)
    }
  }

  def "test Match Results"() {
    expect:
    OutputMarket outputModel = mapper.map(event, market)
    result == outputModel.getHandicapType()

    where:
    event                                          | market                                                    | result
    new Event().tap { categoryCode = 'FOOTBALL' }  | new Market().tap {
      marketMeaningMinorCode = 'MH'
      templateMarketName = 'Handicap Match Result'
    }    | 'matchResult'
    new Event().tap { categoryCode = 'FOOTBALL' }  | new Market().tap {
      marketMeaningMinorCode = 'MH'
      templateMarketName = 'Handicap First Half'
    }      | 'firstHalf'
    new Event().tap { categoryCode = 'FOOTBALL' }  | new Market().tap {
      marketMeaningMinorCode = 'MH'
      templateMarketName = 'Handicap Second Half'
    }     | 'secondHalf'
    new Event().tap { categoryCode = 'SOMESPORT' } | new Market().tap {
      marketMeaningMinorCode = 'MH'
      templateMarketName = 'Handicap Second Half'
    }     | null
    new Event().tap { categoryCode = null }        | new Market().tap {
      marketMeaningMinorCode = 'MH'
      templateMarketName = 'Handicap Second Half'
    }     | null
    new Event().tap { categoryCode = 'FOOTBALL' }  | new Market().tap {
      marketMeaningMinorCode = 'AA'
      templateMarketName = 'Handicap Second Half'
    }     | null
    new Event().tap { categoryCode = 'FOOTBALL' }  | new Market().tap {
      marketMeaningMinorCode = 'MH'
      templateMarketName = 'some that does not exist'
    } | null
  }
}
