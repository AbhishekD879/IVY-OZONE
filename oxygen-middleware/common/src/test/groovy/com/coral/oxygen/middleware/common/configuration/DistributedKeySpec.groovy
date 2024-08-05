package com.coral.oxygen.middleware.common.configuration

import spock.lang.Specification

class DistributedKeySpec extends Specification {

  def "Distributed Name does not exists"() {

    expect:
    !DistributedKey.fromString("test-test").isPresent()
  }

  def "Getting distributed name"() {
    given:
    def expected = DistributedKey.INPLAY_STRUCTURE_MAP
    def actual = DistributedKey.fromString("inplay_structure").get()

    expect:
    actual == expected
  }
}
