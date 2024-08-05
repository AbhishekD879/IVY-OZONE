package com.oxygen.middleware.common.mappers

import com.coral.oxygen.middleware.common.mappers.MarketMapper
import com.coral.oxygen.middleware.common.mappers.MarketNextScoreMapper
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService
import com.coral.oxygen.middleware.common.utils.OrdinalToNumberConverter
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.egalacoral.spark.siteserver.model.Event
import com.egalacoral.spark.siteserver.model.Market
import com.fasterxml.jackson.core.type.TypeReference
import com.fasterxml.jackson.databind.ObjectMapper
import com.google.gson.GsonBuilder
import org.springframework.core.io.ClassPathResource
import spock.lang.Specification

class MarketNextScoreMapperSpec extends Specification {

  MarketTemplateNameService marketTemplateNameService = Mock()
  MarketNextScoreMapper mapper
  OrdinalToNumberConverter ordinalToNumberConverter
  final static String ORDINAL_TO_NUMBER_RESOURCE = 'ordinalToNumber.json'

  MarketMapper chain = Mock()

  def setup() {
    chain.map(_, _) >> new OutputMarket()
    ordinalToNumberConverter = new OrdinalToNumberConverter(new ClassPathResource(ORDINAL_TO_NUMBER_RESOURCE), new GsonBuilder().create())
    mapper = new MarketNextScoreMapper(chain, ordinalToNumberConverter, marketTemplateNameService)

    marketTemplateNameService.containsName(_, _) >> { templateType, marketName ->
      def expectedTemplateName = templateType.toString().replaceAll('_', ' ')
      return expectedTemplateName.equalsIgnoreCase(marketName)
    }
  }

  def "Test match next score"() {
    expect:
    OutputMarket outputMarket = mapper.map(event, market)
    result == outputMarket.getNextScore()

    where:
    event                                           | market                                                            | result
    new Event()                                     |  new Market().tap { templateMarketName = 'Next Team to Score' }   | null
    new Event().tap { categoryCode = 'FOOTBALL' }   |  new Market()                                                     | null
    new Event().tap { categoryCode = 'FOOTBALL' }   |  new Market().tap {
      templateMarketName = 'Next Team to Score'
      name = 'Next Team To Score Goal 15'
    }            | 15
    new Event().tap { categoryCode = 'FOOTBALL' }   |  new Market().tap {
      templateMarketName = 'Next Team to Score'
      name = 'Next Team To Score Goal15'
    }             | null
    new Event().tap { categoryCode = 'FOOTBALL' }   |  new Market().tap {
      templateMarketName = 'Next Team to Score'
      name = 'Thirtieth Team To Score'
    }               | 30
    new Event().tap { categoryCode = 'FOOTBALL' }   |  new Market().tap {
      templateMarketName = 'Next Team to Score'
      name = 'twEnty-ThiRD Team To Score'
    }            | 23
    new Event().tap { categoryCode = 'FOOTBALL' }   |  new Market().tap {
      templateMarketName = 'Next Team to Score'
      name = 'InvalidOrdinalNumber Team To Score'
    }    | null
    new Event().tap { categoryCode = 'FOOTBALL' }   |  new Market().tap {
      templateMarketName = 'Next Team to Score'
      name = ''
    }                                      | null
    new Event().tap { categoryCode = 'FOOTBALL' }   |  new Market().tap {
      templateMarketName = 'Next Team to Score'
      name = 'Next Team To Score Goal'
    }               | null
  }

  def "Test of correct score numbers during parsing of dictionary map"() {
    given:
    def event = new Event().tap { categoryCode='FOOTBALL' }
    List<Market> markets = new ArrayList<>()
    try {
      InputStream dictionary = getClass().getClassLoader().getResourceAsStream(ORDINAL_TO_NUMBER_RESOURCE)
      Map<String, Integer> ordinalNamesMap = new ObjectMapper().readValue(dictionary, new TypeReference<Map<String, Integer>>(){ })
      ordinalNamesMap.each { ordinal, number ->
        Market market = new Market().tap {
          templateMarketName = 'Next Team to Score'
          name = ordinal + ' Team to Score'
        }

        markets.add(market)
      }

      markets.each { market ->
        when:
        OutputMarket outputMarket = mapper.map(event, market)

        then:
        null != outputMarket.getNextScore()
      }
    } catch (Exception e) {
      GroovyTestCase.fail(e)
    }
  }
}
