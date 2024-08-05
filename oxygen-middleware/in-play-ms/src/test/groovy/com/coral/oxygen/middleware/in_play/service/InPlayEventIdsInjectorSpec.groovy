package com.coral.oxygen.middleware.in_play.service

import com.coral.oxygen.middleware.in_play.service.injector.InPlayEventIdsInjector
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData
import spock.lang.Specification

import java.util.stream.Collectors
import java.util.stream.LongStream

class InPlayEventIdsInjectorSpec extends Specification {
  InPlayEventIdsInjector dataInjector

  def setup() {
    dataInjector = new InPlayEventIdsInjector()
  }

  def "Test event counts set by type"() {
    InPlayData data = TestTools.inPlayDataFromFile("InPlayEventIdsInjectorTest/inputData.json")

    when:
    dataInjector.injectData(data)

    then:
    inclusiveSetOfRange(1, 8) ==  new HashSet(data.getLivenow().getEventsIds())

    inclusiveSetOfRange(1, 4) == new HashSet(data.getLivenow().getSportEvents().get(0).getEventsIds())
    inclusiveSetOfRange(5, 8) == new HashSet(data.getLivenow().getSportEvents().get(1).getEventsIds())

    inclusiveSetOfRange(1, 2) == new HashSet(data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getEventsIds())
    inclusiveSetOfRange(3, 4) == new HashSet(data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(1).getEventsIds())
    inclusiveSetOfRange(5, 6) == new HashSet(data.getLivenow().getSportEvents().get(1).getEventsByTypeName().get(0).getEventsIds())
    inclusiveSetOfRange(7, 8) == new HashSet(data.getLivenow().getSportEvents().get(1).getEventsByTypeName().get(1).getEventsIds())

    inclusiveSetOfRange(9, 16) == new HashSet(data.getUpcoming().getEventsIds())

    inclusiveSetOfRange(9, 12) == new HashSet(data.getUpcoming().getSportEvents().get(0).getEventsIds())
    inclusiveSetOfRange(13, 16) == new HashSet(data.getUpcoming().getSportEvents().get(1).getEventsIds())

    inclusiveSetOfRange(9, 10) == new HashSet(data.getUpcoming().getSportEvents().get(0).getEventsByTypeName().get(0).getEventsIds())
    inclusiveSetOfRange(11, 12) == new HashSet(data.getUpcoming().getSportEvents().get(0).getEventsByTypeName().get(1).getEventsIds())
    inclusiveSetOfRange(13, 14) == new HashSet(data.getUpcoming().getSportEvents().get(1).getEventsByTypeName().get(0).getEventsIds())
    inclusiveSetOfRange(15, 16) == new HashSet(data.getUpcoming().getSportEvents().get(1).getEventsByTypeName().get(1).getEventsIds())
  }

  private Set<Long> inclusiveSetOfRange(long from, long to) {
    return LongStream.rangeClosed(from, to).boxed().collect(Collectors.toSet())
  }
}
