package com.oxygen.middleware.common.mappers

import com.coral.oxygen.middleware.common.mappers.EventIsLiveMapper
import com.coral.oxygen.middleware.common.mappers.EventMapper
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.egalacoral.spark.siteserver.model.Event
import spock.lang.Specification

class EventIsLiveMapperSpec extends Specification {

  EventIsLiveMapper mapper
  EventMapper eventMapper = Mock()

  def setup() {
    eventMapper.map(_, _) >> new EventsModuleData()
    mapper = new EventIsLiveMapper(eventMapper)
  }

  def "Test Event is live Mapper"() {
    expect:
    def moduleDataItem = mapper.map(null, event)
    result == moduleDataItem.getEventIsLive()

    where:
    event                                   | result
    new Event()                             | false
    new Event().tap { rawIsOffCode = '-' }  | false
    new Event().tap { rawIsOffCode = 'Y' }  | true
    new Event().tap {
      rawIsOffCode = '-'
      isStarted = Boolean.TRUE
    }                                   | true
    new Event().tap {
      rawIsOffCode = '-'
      isStarted = Boolean.FALSE
    }                                 | false
  }
}
