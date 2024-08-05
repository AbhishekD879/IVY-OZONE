package com.coral.oxygen.edp.model.mapping

import com.coral.oxygen.edp.model.output.OutputEvent
import com.egalacoral.spark.siteserver.model.Event
import spock.lang.Specification

import java.time.Clock
import java.time.LocalDateTime
import java.time.ZoneOffset

import static com.coral.oxygen.edp.TestUtil.deserializeWithJackson

class VirtualEventMapperSpec extends Specification {

  private static final int ONE_MILLISECOND = 1000

  private static final int MINUTES_UNTIL_EVENT = 5
  private static final int MINUTES_UNTIL_EVENT_COMPENSATED_SECONDS = MINUTES_UNTIL_EVENT * 60 - 1

  def chain = Mock(EventMapper)
  def virtualEventMapper = new VirtualEventMapper(chain)

  def "Mapper adds correct value to field millisUntilStart"() {

    given: 'prepare event with start time in 5 minutes, UTC timezone'

    Event event = deserializeWithJackson("/virtuals/event_virtual_raw.json", Event.class)

    event.startTime = LocalDateTime.now(Clock.systemUTC())
        .atZone(ZoneOffset.UTC)
        .plusMinutes(MINUTES_UNTIL_EVENT)
        .toString()

    when: 'map the Event to OutputEvent'

    OutputEvent outputEvent = new OutputEvent()
    virtualEventMapper.populate(outputEvent, event)
    int secUntilStart = (int) (outputEvent.millisUntilStart / ONE_MILLISECOND)

    then: 'mapped outputEvent should have a field millisUntilStart with value of 5 minutes minus one second (299 sec)'

    secUntilStart == MINUTES_UNTIL_EVENT_COMPENSATED_SECONDS
  }
}
