package com.coral.oxygen.middleware.in_play.service.model

import com.coral.oxygen.middleware.pojos.model.output.PrimaryMarkets
import spock.lang.Specification

class PrimaryMarketsSpec extends Specification {

  def "Check Primary Markets"() {

    expect:
    null == PrimaryMarkets.enumerize("non")
    PrimaryMarkets.FOOTBALL == PrimaryMarkets.enumerize("FOOTBALL")
  }
}
