package com.coral.oxygen.middleware.featured.service

import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome
import com.coral.oxygen.middleware.pojos.model.output.OutputPrice
import org.apache.commons.lang3.ObjectUtils
import spock.lang.Specification

import static org.apache.commons.lang3.ObjectUtils.*

class OutcomeOrderingSpec extends Specification {
  private OutcomeOrdering ordering = new OutcomeOrdering()

  def "Ordering empty outcomes is passing"() {
    expect:
    ArrayList<OutputOutcome> outcomes = new ArrayList<>()
    ordering.orderOutcomes(outcomes, true, true)
  }

  def "Ordering by outcome price asc"() {
    ArrayList<OutputOutcome> outcomes = new ArrayList<>()
    outcomes.add(createOutcome("--", 2, 55, "Horse 1", null))
    outcomes.add(createOutcome("--", 1, 15, "Horse 2", null))

    when:
    ordering.orderOutcomes(outcomes, true, true)

    then:
    "Horse 2" == outcomes.get(0).getName()
  }

  def "Ordering by outcome price - nulls last"() {
    ArrayList<OutputOutcome> outcomes = new ArrayList<>()
    OutputOutcome outputOutcome = new OutputOutcome()
    ArrayList<OutputPrice> prices = new ArrayList<>()
    prices.add(null)
    outputOutcome.setPrices(prices)
    outcomes.add(outputOutcome)
    outcomes.add(createOutcome("--", 1, 15, "Horse 2", null))

    when:
    ordering.orderOutcomes(outcomes, true, true)

    then:
    "Horse 2" == outcomes.get(0).getName()
  }

  def "Order outcomes by name asc if prices same"() {
    ArrayList<OutputOutcome> outcomes = new ArrayList<>()
    outcomes.add(createOutcome("--", 2, 5, "Horse 2", null))
    outcomes.add(createOutcome("--", 2, 5, "Horse 1", null))

    when:
    ordering.orderOutcomes(outcomes, true, true)

    then:
    "Horse 1" == outcomes.get(0).getName()
  }

  def "Order outcomes - prices same, name null gets last"() {
    ArrayList<OutputOutcome> outcomes = new ArrayList<>()
    outcomes.add(createOutcome("--", 2, 5, null, null))
    outcomes.add(createOutcome("--", 2, 5, "Horse 1", null))

    when:
    ordering.orderOutcomes(outcomes, true, true)

    then:
    "Horse 1" == outcomes.get(0).getName()
  }

  def "Order outcomes name NR case"() {
    ArrayList<OutputOutcome> outcomes = new ArrayList<>()
    outcomes.add(createOutcome("--", 1, 25, "Horse 2", null))
    outcomes.add(createOutcome("--", 6, 10, "N/R", null))
    outcomes.add(createOutcome("--", 1, 15, "Horse 1", null))

    when:
    ordering.orderOutcomes(outcomes, true, true)

    then:
    "N/R" == outcomes.get(2).getName()
  }

  def "Order outcomes - outcomeMeaningMinorCode go to the end of the list"() {
    ArrayList<OutputOutcome> outcomes = new ArrayList<>()
    outcomes.add(createOutcome("--", 1, 25, "Horse 2", null))
    outcomes.add(createOutcome("--", 1, 5, "Horse 4", null))
    outcomes.add(createOutcome("1", 6, 10, "Horse 3", null))
    outcomes.add(createOutcome("2", 1, 15, "Horse 1", null))

    when:
    ordering.orderOutcomes(outcomes, true, true)

    then:
    "Horse 3" == outcomes.get(2).getName()
    "Horse 1" == outcomes.get(3).getName()
  }

  def "Order outcomes checking complex ordering - case 1"() {
    ArrayList<OutputOutcome> outcomes = new ArrayList<>()
    outcomes.add(createOutcome("--", 1, 25, "Horse 2", null))
    outcomes.add(createOutcome("--", 1, 5, "Horse 4", null))
    outcomes.add(createOutcome("--", 6, 10, "N/R", null))
    outcomes.add(createOutcome("1", 6, 10, "N/R", null))
    outcomes.add(createOutcome("1", 6, 10, "Horse 3", null))
    outcomes.add(createOutcome("2", 1, 15, "Horse 1", null))

    when:
    ordering.orderOutcomes(outcomes, true, true)

    then:
    "Horse 4" == outcomes.get(0).getName()
    "Horse 3" == outcomes.get(2).getName()
    "Horse 1" == outcomes.get(3).getName()
    "N/R" == outcomes.get(4).getName()
    "N/R" == outcomes.get(5).getName()
  }

  def "Order outcomes checking complex ordering - case 2"() {
    ArrayList<OutputOutcome> outcomes = new ArrayList<>()
    outcomes.add(createOutcome("--", 1, 25, "Horse 2", null))
    outcomes.add(createOutcome("--", 1, 5, "Horse 4", null))
    outcomes.add(createOutcome("1", 6, 10, "Horse 3", null))
    outcomes.add(createOutcome("2", 1, 15, "Horse 1", null))
    outcomes.add(createOutcome("--", 6, 10, "N/R", null))
    outcomes.add(createOutcome("--", 6, 100, "N/R", null))
    outcomes.add(createOutcome("--", 1, 2, null, null))

    when:
    ordering.orderOutcomes(outcomes, false, true)

    then:
    "Horse 2" == outcomes.get(0).getName()
    "Horse 4" == outcomes.get(1).getName()
    null == outcomes.get(2).getName()
    "Horse 3" == outcomes.get(3).getName()
    "Horse 1" == outcomes.get(4).getName()
  }

  def "Order outcomes checking when lp not available"() {
    ArrayList<OutputOutcome> outcomes = new ArrayList<>()
    outcomes.add(createOutcome("--", 1, 25, "Horse 2", 1))
    outcomes.add(createOutcome("--", 1, 5, "Horse 4", 3))
    outcomes.add(createOutcome("1", 6, 10, "Horse 3", 4))
    outcomes.add(createOutcome("2", 1, 15, "Horse 1", 2))
    outcomes.add(createOutcome("--", 6, 10, "N/R", null))
    outcomes.add(createOutcome("1", 6, 10, "N/R", null))
    outcomes.add(createOutcome("--", 1, 2, null, null))

    when:
    this.ordering.orderOutcomes(outcomes, false, true)

    then:
    null == outcomes.get(0).getName()
    "Horse 2" == outcomes.get(1).getName()
    "Horse 4" == outcomes.get(2).getName()
    "Horse 3" == outcomes.get(3).getName()
    "Horse 1" == outcomes.get(4).getName()
    "N/R" == outcomes.get(5).getName()
  }

  def "Order  RacingGrid outcomes with sp"() {
    ArrayList<OutputOutcome> outcomes = new ArrayList<>()
    outcomes.add(createOutcome("--", null, null, "Horse 2", 1))
    outcomes.add(createOutcome("--", null, null, "Horse 4", 3))
    outcomes.add(createOutcome("1", null, null, "Horse 3", 4))
    outcomes.add(createOutcome("2", null, null, "Horse 1", 2))
    outcomes.add(createOutcome("--", null, null, "N/R", null))
    outcomes.add(createOutcome("1", null, null, "N/R", null))

    when:
    ordering.orderRacingGridOutcomes(outcomes, true)

    then:
    int i = 0
    "Horse 1" == outcomes.get(i++).getName()
    "Horse 2" == outcomes.get(i++).getName()
    "Horse 3" == outcomes.get(i++).getName()
    "Horse 4" == outcomes.get(i++).getName()
    "N/R" == outcomes.get(i++).getName()
    "N/R" == outcomes.get(i++).getName()
  }

  def "Order RacingGrid outcomes with lp"() {
    ArrayList<OutputOutcome> outcomes = new ArrayList<>()
    outcomes.add(createOutcome("2", 1, 15, "Horse 1", 1))
    outcomes.add(createOutcome("--", 1, 25, "Horse 2", 2))
    outcomes.add(createOutcome("1", 6, 10, "Horse 3", 3))
    outcomes.add(createOutcome("--", 1, 5, "Horse 4", 4))
    outcomes.add(createOutcome("--", 6, 10, "N/R", null))
    outcomes.add(createOutcome("1", 6, 10, "N/R", null))
    outcomes.add(createOutcome("--", 1, 2, null, null))

    when:
    ordering.orderRacingGridOutcomes(outcomes, false)

    then:
    int i = 0
    null == outcomes.get(i++).getName()
    "Horse 4" == outcomes.get(i++).getName()
    "Horse 1" == outcomes.get(i++).getName()
    "Horse 3" == outcomes.get(i++).getName()
    "N/R" == outcomes.get(i++).getName()
    "N/R" == outcomes.get(i++).getName()
    "Horse 2" == outcomes.get(i++).getName()
  }

  private static OutputOutcome createOutcome(String mmCode, Integer priceDen, Integer priceNum, String name,
      Integer runnerNumber) {
    OutputOutcome outputOutcome = new OutputOutcome()
    outputOutcome.setName(name)
    outputOutcome.setRunnerNumber(runnerNumber)
    outputOutcome.setOutcomeMeaningMinorCode(mmCode)
    ArrayList<OutputPrice> prices = new ArrayList<>()
    OutputPrice e = new OutputPrice()
    e.setPriceDen(priceDen)
    e.setPriceNum(priceNum)
    e.setPriceDec(defaultIfNull(priceDen, 0) + defaultIfNull(priceNum, 0))
    prices.add(e)
    outputOutcome.setPrices(prices)
    return outputOutcome
  }
}
