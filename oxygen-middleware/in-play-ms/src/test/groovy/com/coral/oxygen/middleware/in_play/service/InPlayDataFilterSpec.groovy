package com.coral.oxygen.middleware.in_play.service

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayModel
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment
import spock.lang.Specification

class InPlayDataFilterSpec extends Specification {

  InPlayDataFilter dataFilter

  InPlayData data

  def setup() {
    data = new InPlayData(new InPlayModel(), new InPlayModel(), new InPlayModel(), new InPlayModel())
    dataFilter = new InPlayDataFilter()
  }

  def cleanup() {
    dataFilter = null
  }

  def "Remove empty sport"() {
    setup:
    data.getLivenow().getSportEvents().add(new SportSegment())
    data.getUpcoming().getSportEvents().add(new SportSegment())
    data.getLiveStream().getSportEvents().add(new SportSegment())

    when:
    dataFilter.removeEmptyNodes(data)

    then:
    0 == data.getLivenow().getSportEvents().size()
    0 == data.getUpcoming().getSportEvents().size()
    0 == data.getLiveStream().getSportEvents().size()
  }

  def "Remove Empty Types"() {
    setup:
    data.getLivenow().getSportEvents().add(new SportSegment())
    data.getUpcoming().getSportEvents().add(new SportSegment())
    data.getLiveStream().getSportEvents().add(new SportSegment())

    data.getLivenow().getSportEvents().get(0).getEventsByTypeName().add(new TypeSegment())
    data.getLivenow().getSportEvents().get(0).getEventsByTypeName().add(new TypeSegment())
    data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getEvents().add(new EventsModuleData())

    data.getUpcoming().getSportEvents().get(0).getEventsByTypeName().add(new TypeSegment())
    data.getUpcoming().getSportEvents().get(0).getEventsByTypeName().add(new TypeSegment())
    data.getUpcoming().getSportEvents().get(0).getEventsByTypeName().get(0).getEvents().add(new EventsModuleData())

    data.getLiveStream().getSportEvents().get(0).getEventsByTypeName().add(new TypeSegment())
    data.getLiveStream().getSportEvents().get(0).getEventsByTypeName().add(new TypeSegment())
    data.getLiveStream().getSportEvents().get(0).getEventsByTypeName().get(0).getEvents().add(new EventsModuleData())

    when:
    dataFilter.removeEmptyNodes(data)

    then:
    1 == data.getLivenow().getSportEvents().get(0).getEventsByTypeName().size()
    !data.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getEvents().isEmpty()
    1 == data.getUpcoming().getSportEvents().get(0).getEventsByTypeName().size()
    !data.getUpcoming().getSportEvents().get(0).getEventsByTypeName().get(0).getEvents().isEmpty()
    1 == data.getLiveStream().getSportEvents().get(0).getEventsByTypeName().size()
    !data.getLiveStream().getSportEvents().get(0).getEventsByTypeName().get(0).getEvents().isEmpty()
  }
}
