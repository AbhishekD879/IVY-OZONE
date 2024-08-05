package com.oxygen.middleware.common.mappers

import com.coral.oxygen.middleware.common.mappers.OutcomeCorrectPriceTypeMapper
import com.coral.oxygen.middleware.common.mappers.OutcomeMapper
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome
import com.egalacoral.spark.siteserver.model.Market
import com.egalacoral.spark.siteserver.model.Outcome
import com.egalacoral.spark.siteserver.model.Price
import spock.lang.Specification

class OutcomeCorrectPriceTypeMapperSpec extends Specification {

  OutcomeCorrectPriceTypeMapper mapper

  OutcomeMapper chain = Mock()

  def setup(){
    chain.map(_,_,_) >> new OutputOutcome()

    mapper = new OutcomeCorrectPriceTypeMapper(chain)
  }

  def "Test Correct Price Type"() {

    expect:
    OutputOutcome outputOutcome = mapper.map(null, market, outcome)
    result == outputOutcome.getCorrectPriceType()

    where:
    market                                    | outcome                                                  | result
    new Market().tap { isSpAvailable = true } | new Outcome()                                            | "SP"
    new Market().tap { isLpAvailable = true } | new Outcome() {
      @Override
      List<Price> getPrices() {
        return new ArrayList<Price>().tap { add(new Price()) }
      }
    }                                                        | "LP"
    new Market().tap { isLpAvailable = false } | new Outcome() {
      @Override
      List<Price> getPrices() {
        return new ArrayList<Price>().tap { add(new Price()) }
      }
    }                                                        | null
    new Market().tap {
      isSpAvailable = true
      isLpAvailable = true
    }       | new Outcome() {
      @Override
      List<Price> getPrices() {
        return null
      }
    }                                                        | "SP"
  }

  def "Test Correct Price Type1"() {

    expect:
    OutputOutcome outputOutcome = mapper.map(null, market, outcome)
    result == outputOutcome.getCorrectPriceType()

    where:
    market                                    | outcome                                                  | result
    new Market().tap {
      isLpAvailable = true
      isSpAvailable = true
    } | new Outcome() {
      @Override
      List<Price> getPrices() {
        return new ArrayList<Price>().tap { add(new Price()) }
      }
    }                                                        | "LP"

    new Market().tap { isLpAvailable = false} | new Outcome() {
      @Override
      List<Price> getPrices() {
        return null
      }
    }                                                        | null

    new Market().tap { isLpAvailable = true} | new Outcome() {
      @Override
      List<Price> getPrices() {
        return null
      }
    }                                                        | null

    new Market().tap {
      isSpAvailable = true
      isLpAvailable = false
    }       | new Outcome() {
      @Override
      List<Price> getPrices() {
        return null
      }
    }                                                        | "SP"

    new Market().tap {
      isSpAvailable = false
      isLpAvailable = true
    }       | new Outcome() {
      @Override
      List<Price> getPrices() {
        return null
      }
    }                                                        | null

    new Market().tap {
      isSpAvailable = false
      isLpAvailable = false
    }       | new Outcome() {
      @Override
      List<Price> getPrices() {
        return null
      }
    }                                                        | null

    new Market().tap {
      isLpAvailable = true
      isSpAvailable = false
    } | new Outcome() {
      @Override
      List<Price> getPrices() {
        return new ArrayList<Price>().tap { add(new Price()) }
      }
    }                                                        | "LP"

    new Market().tap {
      isLpAvailable = false
      isSpAvailable = true
    } | new Outcome() {
      @Override
      List<Price> getPrices() {
        return new ArrayList<Price>().tap { add(new Price()) }
      }
    }                                                        | "SP"

    new Market().tap {
      isLpAvailable = false
      isSpAvailable = false
    } | new Outcome() {
      @Override
      List<Price> getPrices() {
        return new ArrayList<Price>().tap { add(new Price()) }
      }
    }                                                        | null
  }
}
