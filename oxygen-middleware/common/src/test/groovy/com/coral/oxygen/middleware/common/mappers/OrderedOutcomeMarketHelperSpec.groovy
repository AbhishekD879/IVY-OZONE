package com.coral.oxygen.middleware.common.mappers

import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.Children
import com.egalacoral.spark.siteserver.model.Event
import com.egalacoral.spark.siteserver.model.Market
import com.egalacoral.spark.siteserver.model.Outcome
import spock.lang.Specification

class OrderedOutcomeMarketHelperSpec extends Specification {

  SiteServerApi siteServerApi = Mock()

  OrderedOutcomeMarketHelper helper = new OrderedOutcomeMarketHelper(siteServerApi)


  def "Recalculate Corrected Meaning Minor Code - outcomes more than 2"() {

    given:
    Event event = new Event()
    event.name = "Test Event"
    OutputMarket market = new OutputMarket()
    OutputOutcome outcome = new OutputOutcome()
    outcome.setDisplayOrder(1)
    OutputOutcome outcome1 = new OutputOutcome()
    outcome1.setDisplayOrder(2)
    OutputOutcome outcome2 = new OutputOutcome()
    outcome2.setDisplayOrder(3)
    OutputOutcome outcome3 = new OutputOutcome()
    outcome3.setDisplayOrder(4)
    market.setOutcomes(Arrays.asList(outcome, outcome1, outcome2, outcome3))

    when:
    helper.recalculateCorrectedMeaningMinorCode(event, market)

    then:
    market.getOutcomes().get(0).getCorrectedOutcomeMeaningMinorCode() == 1
    market.getOutcomes().get(1).getCorrectedOutcomeMeaningMinorCode() == 2
    market.getOutcomes().get(2).getCorrectedOutcomeMeaningMinorCode() == null
    market.getOutcomes().get(3).getCorrectedOutcomeMeaningMinorCode() == 3
  }

  def "Recalculate Corrected Meaning Minor Code - outcomes less than 2"() {
    given:
    OutputMarket outputMarket = new OutputMarket()
    outputMarket.setId("marketId-123")
    OutputOutcome outputOutcome = new OutputOutcome()
    outputOutcome.setDisplayOrder(1)
    OutputOutcome outputOutcome1 = new OutputOutcome()
    outputOutcome1.setDisplayOrder(2)
    outputMarket.setOutcomes(Arrays.asList(outputOutcome, outputOutcome1))

    Outcome outcome1 = new Outcome()
    outcome1.displayOrder = 1

    Outcome outcome2 = new Outcome()
    outcome2.displayOrder = 2

    Outcome outcome3 = new Outcome()
    outcome3.displayOrder = 3

    Children childOutcome1 = new Children()
    childOutcome1.outcome = outcome1
    Children childOutcome2 = new Children()
    childOutcome2.outcome = outcome2

    Children childOutcome3 = new Children()
    childOutcome3.outcome = outcome3

    Market market1 = new Market()
    market1.name = "market1"
    market1.displayOrder = 10
    market1.children = Arrays.asList(childOutcome1)


    Market market2 = new Market()
    market2.name = "market2"
    market2.displayOrder = 100
    market2.children = Arrays.asList(childOutcome2)

    Market market3 = new Market()
    market3.name = "market3"
    market3.displayOrder = 40
    market3.children = Arrays.asList(childOutcome3)


    Children child1 = new Children()
    child1.market = market1
    Children child2 = new Children()
    child2.market = market2

    Children child3 = new Children()
    child3.market = market3


    Event event = new Event()
    event.id = "1"
    event.children = Arrays.asList(child1, child2, child3)
    event.name = "TestEvent"


    Optional<List<Market>> markets = Optional.of(event.getMarkets());

    siteServerApi.getEventToOutcomeForMarket(_, true) >> markets

    when:
    helper.recalculateCorrectedMeaningMinorCode(event, outputMarket)

    then:
    outputMarket.getOutcomes().get(0).getCorrectedOutcomeMeaningMinorCode() == 1
    outputMarket.getOutcomes().get(1).getCorrectedOutcomeMeaningMinorCode() == 2
  }
}
