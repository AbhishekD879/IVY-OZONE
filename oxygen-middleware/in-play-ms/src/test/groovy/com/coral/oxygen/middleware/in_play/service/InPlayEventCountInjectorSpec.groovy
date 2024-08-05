package com.coral.oxygen.middleware.in_play.service

import com.coral.oxygen.middleware.in_play.service.injector.InPlayEventCountInjector
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import spock.lang.Shared
import spock.lang.Specification

class InPlayEventCountInjectorSpec extends Specification {

  @Shared
  InPlayEventCountInjector dataInjector
  @Shared
  InPlayData data

  static final int UPCOMING_SPORT_EVENTS_BY_TYPE_NAME_COUNT = 2
  static
  final int UPCOMING_SPORT_EVENTS_COUNT = UPCOMING_SPORT_EVENTS_BY_TYPE_NAME_COUNT + UPCOMING_SPORT_EVENTS_BY_TYPE_NAME_COUNT
  static final int UPCOMING_EVENT_COUNT = UPCOMING_SPORT_EVENTS_COUNT + UPCOMING_SPORT_EVENTS_COUNT

  static final int LIVE_NOW_SPORT_EVENTS_BY_TYPE_NAME_COUNT = 2
  static
  final int LIVE_NOW_SPORT_EVENTS_COUNT = LIVE_NOW_SPORT_EVENTS_BY_TYPE_NAME_COUNT + LIVE_NOW_SPORT_EVENTS_BY_TYPE_NAME_COUNT
  static final int LIVE_NOW_EVENT_COUNT = LIVE_NOW_SPORT_EVENTS_COUNT + LIVE_NOW_SPORT_EVENTS_COUNT

  def setupSpec() throws Exception {
    dataInjector = new InPlayEventCountInjector()
    data = TestTools.inPlayDataFromFile('InPlayEventIdsInjectorTest/inputData.json')
  }

  def "Should populate event count for live now"() {
    when:
    dataInjector.injectData(data)

    then:
    data.getLivenow().getEventCount() == LIVE_NOW_EVENT_COUNT
  }

  def "Should populate event count for upcoming"() {
    when:
    dataInjector.injectData(data)

    then:
    data.getUpcoming().getEventCount() == UPCOMING_EVENT_COUNT
  }

  def "Should populate event count for sport events of live now"() {
    when:
    dataInjector.injectData(data)
    List<SportSegment> sportEvents = data.getLivenow().getSportEvents()

    then:
    LIVE_NOW_SPORT_EVENTS_COUNT == sportEvents.get(0).getEventCount()
    LIVE_NOW_SPORT_EVENTS_COUNT == sportEvents.get(1).getEventCount()
  }

  def "Should populate event count for sport events of upcoming"() {
    when:
    dataInjector.injectData(data)
    List<SportSegment> sportEvents = data.getUpcoming().getSportEvents()

    then:
    UPCOMING_SPORT_EVENTS_COUNT == sportEvents.get(0).getEventCount()
    UPCOMING_SPORT_EVENTS_COUNT == sportEvents.get(1).getEventCount()
  }

  def "Should populate event count for events by typename of sport events of livenow"() {
    when:
    dataInjector.injectData(data)
    List<SportSegment> sportEvents = data.getLivenow().getSportEvents()

    then:
    LIVE_NOW_SPORT_EVENTS_BY_TYPE_NAME_COUNT ==  sportEvents.get(0).getEventsByTypeName().get(0).getEventCount()
    LIVE_NOW_SPORT_EVENTS_BY_TYPE_NAME_COUNT == sportEvents.get(0).getEventsByTypeName().get(1).getEventCount()
    LIVE_NOW_SPORT_EVENTS_BY_TYPE_NAME_COUNT == sportEvents.get(1).getEventsByTypeName().get(0).getEventCount()
    LIVE_NOW_SPORT_EVENTS_BY_TYPE_NAME_COUNT == sportEvents.get(1).getEventsByTypeName().get(1).getEventCount()
  }

  def "Should populate event count for events by typename of sport events of upcoming"() {
    when:
    dataInjector.injectData(data)
    List<SportSegment> sportEvents = data.getUpcoming().getSportEvents()

    then:
    UPCOMING_SPORT_EVENTS_BY_TYPE_NAME_COUNT == sportEvents.get(0).getEventsByTypeName().get(0).getEventCount()
    UPCOMING_SPORT_EVENTS_BY_TYPE_NAME_COUNT == sportEvents.get(0).getEventsByTypeName().get(1).getEventCount()
    UPCOMING_SPORT_EVENTS_BY_TYPE_NAME_COUNT == sportEvents.get(1).getEventsByTypeName().get(0).getEventCount()
    UPCOMING_SPORT_EVENTS_BY_TYPE_NAME_COUNT == sportEvents.get(1).getEventsByTypeName().get(1).getEventCount()
  }
}
