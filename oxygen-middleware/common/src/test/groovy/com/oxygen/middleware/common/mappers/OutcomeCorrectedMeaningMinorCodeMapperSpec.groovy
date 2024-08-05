package com.oxygen.middleware.common.mappers


import com.coral.oxygen.middleware.common.mappers.OutcomeCorrectedMeaningMinorCodeMapper
import com.coral.oxygen.middleware.common.mappers.OutcomeMapper
import com.coral.oxygen.middleware.common.service.SportsConfig
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome
import com.egalacoral.spark.siteserver.model.Children
import com.egalacoral.spark.siteserver.model.Event
import com.egalacoral.spark.siteserver.model.Market
import com.egalacoral.spark.siteserver.model.Outcome
import com.google.gson.GsonBuilder
import org.springframework.core.io.ClassPathResource
import spock.lang.Specification

class OutcomeCorrectedMeaningMinorCodeMapperSpec extends Specification {

  OutcomeCorrectedMeaningMinorCodeMapper mapper

  OutcomeMapper chain = Mock()

  def setup() {
    chain.map(_, _, _) >> new OutputOutcome()
    SportsConfig sportsConfig = new SportsConfig(new ClassPathResource('sportsConfig.json'), new GsonBuilder().setPrettyPrinting().create())

    mapper = new OutcomeCorrectedMeaningMinorCodeMapper(chain, sportsConfig)
  }

  def "Test Output Outcome"() {
    Market market = new Market()
    Children child1 = new Children()
    Children child2 = new Children()
    Outcome resultOutcome1 = new Outcome()
    Outcome resultOutcome2 = new Outcome()
    List<Children> list = []
    resultOutcome1.id = '123'
    resultOutcome2.id = '456'
    child1.setOutcome(resultOutcome1)
    child2.setOutcome(resultOutcome2)
    list.add(child1)
    list.add(child2)
    market.children = list

    expect:
    OutputOutcome outputOutcome = mapper.map(event, market, outcome)
    result == outputOutcome.getCorrectedOutcomeMeaningMinorCode()

    where:
    event                               | outcome                                        | result
    new Event()                      | new Outcome(outcomeMeaningMinorCode:  'H') | 1
    new Event(typeFlagCodes: 'US')  | new Outcome(outcomeMeaningMinorCode:  'H') | 3
    new Event()                         | new Outcome(outcomeMeaningMinorCode:  'A') | 3
    new Event(typeFlagCodes: 'US') | new Outcome(outcomeMeaningMinorCode:  'A') | 1
    new Event()                         | new Outcome(outcomeMeaningMinorCode:  'D') | 2
    new Event()                         | new Outcome(outcomeMeaningMinorCode:  'N') | 2
    new Event()                         | new Outcome(outcomeMeaningMinorCode:  'L')        | 2
    new Event(typeFlagCodes: 'US') | new Outcome(outcomeMeaningMinorCode: 'L', outcomeMeaningMajorCode: 'HL')      | 1
    new Event()                            | new Outcome(outcomeMeaningMinorCode: 'L', outcomeMeaningMajorCode: 'HL') | 3
    new Event(name:  'A VS B')      | new Outcome(name:  'YES', id: '123')     | 1
    new Event(name:  'A VS B')      | new Outcome(name:  'NO', id: '123')     | 3
    new Event(name:  'A vs B')      | new Outcome(name:  'A', id: '123')     | 1
    new Event(name:  'A vs B')      | new Outcome(name:  'B', id: '456')     | 3
    new Event(name:  'A vs B',categoryId: '19' )     | new Outcome(name:  'B', id: '123')     | null
  }

  def "Test Output Outcome_2"() {
    Market market = new Market()
    Children child1 = new Children()
    Outcome resultOutcome1 = new Outcome()
    List<Children> list = []
    resultOutcome1.id = '123'
    child1.setOutcome(resultOutcome1)
    list.add(child1)
    market.children = list

    expect:
    OutputOutcome outputOutcome = mapper.map(event, market, outcome)
    result == outputOutcome.getCorrectedOutcomeMeaningMinorCode()

    where:

    event                       | outcome                                | result
    new Event(name:  'A vs B')  | new Outcome(name:  'A', id: '123')     | 1
    new Event(name:  'A vs B')  | new Outcome(name:  'B', id: '456')     | 0
  }
}
