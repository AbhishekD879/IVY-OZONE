package com.coral.oxygen.middleware.in_play.service

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import spock.lang.Shared
import spock.lang.Specification

class InPlayDataSorterSpec extends Specification {

  InPlayDataSorter dataSorter
  @Shared
  InPlayData data
  static final int UPCOMING_SPORT_EVENTS_BY_TYPE_NAME_COUNT = 0

  def setup() {
    dataSorter = new InPlayDataSorter()
    data = TestTools.inPlayDataFromFile('InPlayEventIdsInjectorTest/inputData.json')
  }
  def "Test of Sort"() {
    given:
    List<SportSegment> sportSegmentList = data.getUpcoming().getSportEvents()
    when:
    dataSorter.sort(sportSegmentList)
    then:
    UPCOMING_SPORT_EVENTS_BY_TYPE_NAME_COUNT == sportSegmentList.get(0).getEventsByTypeName().get(0).getEventCount()
  }
  // def "Test of Sort"() {
  //       given:
  //   InPlayData data = TestTools.inPlayDataFromFile('InPlayDataSorterTest/inputData.json')

  //       when:
  //   dataSorter.sort(data)

  //       then:
  //   // live sports
  //   10 == data.getLivenow().getSportEvents().get(0).getDisplayOrder()
  //   20 == data.getLivenow().getSportEvents().get(1).getDisplayOrder()

  //   // upcoming sports
  //   11 == data.getUpcoming().getSportEvents().get(0).getDisplayOrder()
  //   21 == data.getUpcoming().getSportEvents().get(1).getDisplayOrder()

  //   // types sorted by type display order with the same class display order
  //   -1501 == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getClassDisplayOrder()
  //   -3 == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeDisplayOrder()
  //   -1501 == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(1).getClassDisplayOrder()
  //   8 == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(1).getTypeDisplayOrder()

  //   // types sorted by class display order
  //   -1600 == data.getLivenow().getSportEvents().get(1).getEventsByTypeName().get(0).getClassDisplayOrder()
  //   0 == data.getLivenow().getSportEvents().get(1).getEventsByTypeName().get(0).getTypeDisplayOrder()
  //   -1500 == data.getLivenow().getSportEvents().get(1).getEventsByTypeName().get(1).getClassDisplayOrder()
  //   0 == data.getLivenow().getSportEvents().get(1).getEventsByTypeName().get(1).getTypeDisplayOrder()

  //   // types sorted in upcoming sports
  //   -1500 == data.getUpcoming().getSportEvents().get(0).getEventsByTypeName().get(0).getClassDisplayOrder()
  //   -9 == data.getUpcoming().getSportEvents().get(0).getEventsByTypeName().get(0).getTypeDisplayOrder()
  //   -1500 == data.getUpcoming().getSportEvents().get(0).getEventsByTypeName().get(1).getClassDisplayOrder()
  //   0 == data.getUpcoming().getSportEvents().get(0).getEventsByTypeName().get(1).getTypeDisplayOrder()

  //   -1600 == data.getUpcoming().getSportEvents().get(1).getEventsByTypeName().get(0).getClassDisplayOrder()
  //   1 == data.getUpcoming().getSportEvents().get(1).getEventsByTypeName().get(0).getTypeDisplayOrder()
  //   -1500 == data.getUpcoming().getSportEvents().get(1).getEventsByTypeName().get(1).getClassDisplayOrder()
  //   0 == data.getUpcoming().getSportEvents().get(1).getEventsByTypeName().get(1).getTypeDisplayOrder()

  //   // events order
  //   TypeSegment typeSegment = data.getLivenow().getSportEvents().get(1).getEventsByTypeName().get(1)
  //   List<EventsModuleData> events = typeSegment.getEvents()
  //   // by start time
  //   '2016-01-26T14:15:00Z' == events.get(0).getStartTime()
  //   '2017-01-26T14:15:00Z' == events.get(1).getStartTime()
  //   '2017-01-26T14:15:00Z' == events.get(2).getStartTime()
  //   '2017-01-26T14:15:00Z' == events.get(3).getStartTime()
  //   null == events.get(4).getStartTime()
  //   null == events.get(5).getStartTime()
  //   null == events.get(6).getStartTime()

  //   // by second ley display order
  //   // for 2017 start time
  //   0 == events.get(1).getDisplayOrder()
  //   10 == events.get(2).getDisplayOrder()
  //   10 == events.get(3).getDisplayOrder()
  //   // for null start time
  //   0 == events.get(4).getDisplayOrder()
  //   5 == events.get(5).getDisplayOrder()
  //   5 == events.get(6).getDisplayOrder()

  //   // for 2017 - 10
  //   'AAA' == events.get(2).getName()
  //   'CCC' == events.get(3).getName()

  //   // for null - 5
  //   'AAA' == events.get(5).getName()
  //   'DDD' == events.get(6).getName()
  // }

}
