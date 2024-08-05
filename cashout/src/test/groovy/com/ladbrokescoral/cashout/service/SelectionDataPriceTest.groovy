package com.ladbrokescoral.cashout.service

import spock.lang.Specification

class SelectionDataPriceTest extends Specification {

  def "When price is <= 1/100 then it's uncompetitive"() {
    expect:
    !new SelectionDataPrice(1, 100).isCompetitive()
    !new SelectionDataPrice(1, 101).isCompetitive()
    !new SelectionDataPrice(1, 1000).isCompetitive()
    !new SelectionDataPrice(2, 200).isCompetitive()
  }

  def "When price is > 1/100 then it's competitive"() {
    expect:
    new SelectionDataPrice(1, 99).isCompetitive()
    new SelectionDataPrice(1, 1).isCompetitive()
    new SelectionDataPrice(2, 199).isCompetitive()
    new SelectionDataPrice(4, 1).isCompetitive()
  }

  def "test price equality"() {
    expect:
    new SelectionDataPrice(1, 2) != null
    new SelectionDataPrice(1, 2) != new SelectionDataPrice(1, 3)
    new SelectionDataPrice(1, 2) != new SelectionDataPrice(3, 2)
    new SelectionDataPrice(3, 4) != new SelectionDataPrice(5, 6)
    new SelectionDataPrice(3, 4) == new SelectionDataPrice(3, 4)
  }
}
