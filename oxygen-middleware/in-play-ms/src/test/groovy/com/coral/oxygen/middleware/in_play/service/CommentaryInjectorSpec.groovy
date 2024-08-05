package com.coral.oxygen.middleware.in_play.service

import com.coral.oxygen.cms.api.SystemConfigProvider
import com.coral.oxygen.middleware.in_play.service.injector.InplayCommentaryInjector
import com.coral.oxygen.middleware.in_play.service.siteserver.InplaySiteServeService
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig
import com.coral.oxygen.middleware.pojos.model.output.Clock
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment
import com.egalacoral.spark.siteserver.model.Event
import spock.lang.Specification

import java.util.function.Function
import java.util.stream.Collectors

class CommentaryInjectorSpec extends Specification {

  InplayCommentaryInjector injector

  InplaySiteServeService siteServeService = Mock()
  SystemConfigProvider systemConfigProvider = Mock()

  CmsSystemConfig cmsSystemConfig

  def setup() {
    Event[] events = TestTools.fromFile('InPlayCommentaryInjectorTest/comments.json', Event[].class)
    siteServeService.getCommentaryForEvent(_ as List) >> Arrays.asList(events).stream().collect(Collectors.toMap({ e -> e.getId() }, Function.identity()))

    cmsSystemConfig = new CmsSystemConfig( )
    cmsSystemConfig.bipScoreEvents = [
      '52': true,
      '36': true,
      '20': true,
      '5': true
    ]

    systemConfigProvider.systemConfig() >> cmsSystemConfig

    injector = new InplayCommentaryInjector(siteServeService, systemConfigProvider)
  }

  def cleanup() {
    injector = null
  }

  def "Football without Start Time Event Period and Response Creation Time"() {
    setup:
    def dataInput = createDummyData(eventId, categoryCode)

    expect:
    injector.injectData(dataInput)
    result == firstEvent(dataInput).getInitClock()

    where:
    eventId  || categoryCode || result
    5006498L || null         || null
    5006498L || 'FOOTBALL'   || null
    1L       || 'FOOTBALL'   || null
    2L       || 'FOOTBALL'   || null
    3L       || 'FOOTBALL'   || null
    100L     || 'FOOTBALL'   || null
  }

  def "Football with null Event Period and Response Creation Time"() {
    setup:
    def input = createDummyData(5006498L, 'FOOTBALL')
    firstEvent(input).setStartTime(null)
    firstEvent(input).setResponseCreationTime(null)

    when:
    injector.injectData(input)

    then:
    null == firstEvent(input).getInitClock()
  }

  def "Remove provider marker from inplay upcoming event"() {
    setup:
    def input = createUpcomingInplayDataWithEvent('Boston Red Sox @ *Philadelphia Phillies(SS)', 'BASEBALL', '5')

    when:
    injector.injectData(input)

    then:
    !firstUpcomingEvent(input).getName().contains('(SS)')
  }

  def "Football: check Clock Data"() {
    setup:
    def input = createDummyData(5006498L, 'FOOTBALL')
    firstEvent(input).setStartTime('2017-01-30T19:45:00Z')
    firstEvent(input).setResponseCreationTime('2017-01-30T20:08:22.369Z')

    when:
    injector.injectData(input)
    Clock clock = firstEvent(input).getInitClock()

    then:
    null != clock
    'football' == clock.getSport()
    5006498L == clock.getEv_id()
    '2017-01-30T20:01:23Z' == clock.getLast_update()
    'FIRST_HALF' == clock.getPeriod_code()
    'S' == clock.getState()
    '869' == clock.getClock_seconds()
    '1485806483' == clock.getLast_update_secs()
    '1485805500' == clock.getStart_time_secs()
    '1288' == clock.getOffset_secs()
  }

  // -------- helpers ----------
  InPlayData createDummyData(Long eventId, String categoryCode) {
    InPlayData data = new InPlayData()
    SportSegment sportSegment = new SportSegment()
    TypeSegment typeSegment = new TypeSegment()
    sportSegment.getEventsByTypeName().add(typeSegment)

    EventsModuleData event = new EventsModuleData()
    event.setId(eventId)
    event.setCategoryCode(categoryCode)
    typeSegment.getEvents().add(event)

    data.getLivenow().getSportEvents().add(sportSegment)
    return data
  }

  InPlayData createUpcomingInplayDataWithEvent(String eventName, String categoryCode, String categoryId) {
    InPlayData data = new InPlayData()
    SportSegment sportSegment = new SportSegment()
    TypeSegment typeSegment = new TypeSegment()
    sportSegment.getEventsByTypeName().add(typeSegment)

    EventsModuleData event = new EventsModuleData()
    event.setName(eventName)
    event.setCategoryCode(categoryCode)
    event.setCategoryId(categoryId)
    typeSegment.getEvents().add(event)

    data.getUpcoming().getSportEvents().add(sportSegment)
    return data
  }

  EventsModuleData firstEvent(InPlayData data) {
    return data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getEvents().get(0)
  }

  EventsModuleData firstUpcomingEvent(InPlayData data) {
    return data.getUpcoming().getSportEvents().get(0).getEventsByTypeName().get(0).getEvents().get(0)
  }

}
