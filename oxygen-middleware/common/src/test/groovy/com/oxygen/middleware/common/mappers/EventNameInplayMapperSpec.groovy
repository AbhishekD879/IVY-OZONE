package com.oxygen.middleware.common.mappers

import com.coral.oxygen.middleware.common.mappers.EventMapper
import com.coral.oxygen.middleware.common.mappers.EventNameInplayMapper
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import spock.lang.Shared
import spock.lang.Specification

class EventNameInplayMapperSpec extends Specification {

  EventNameInplayMapper mapper

  EventMapper eventMapper = Mock()

  @Shared EventsModuleData moduleDataItemMock

  def setup() {
    moduleDataItemMock = new EventsModuleData()
    eventMapper.map(_,_) >> moduleDataItemMock
    mapper = new EventNameInplayMapper(eventMapper)
  }

  def "Test Event Name Inplay: Check Event Names"() {

    expect:
    moduleDataItemMock.setName(name)
    moduleDataItemMock.setNameOverride(nameOverride)
    def moduleDataItem = mapper.map(moduleDataItemMock, null)
    result == moduleDataItem.getName()

    where:
    name            | nameOverride    | result
    null            | null            |  null
    "play-off"      | null            | "play-off"
    null            | "over-play-off" | "over-play-off"
  }
}
