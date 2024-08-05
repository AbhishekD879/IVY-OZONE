package com.oxygen.middleware.common.mappers

import com.coral.oxygen.middleware.common.mappers.MarketMapper
import com.coral.oxygen.middleware.common.mappers.MarketTermsMapper
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.egalacoral.spark.siteserver.model.Market
import spock.lang.Specification

class MarketTermsMapperSpec extends Specification {

  MarketTermsMapper mapper

  MarketMapper chain = Mock()

  def setup() {
    chain.map(_, _) >> new OutputMarket()
    mapper = new MarketTermsMapper(chain)
  }

  def "Test Terms"() {
    expect:
    OutputMarket outputMarket = mapper.map(null, market)
    result == outputMarket.getTerms()

    where:
    market                                    | result
    new Market().tap { eachWayPlaces = null } | null
    new Market().tap {
      eachWayPlaces = 5
      eachWayFactorNum = 11
      eachWayFactorDen = 22
    } | 'Each Way: 11/22 odds - places 1,2,3,4,5'
  }
}
