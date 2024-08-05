package com.oxygen.middleware.common.mappers

import com.coral.oxygen.middleware.common.mappers.EventLiveStreamAvailableMapper
import com.coral.oxygen.middleware.common.mappers.EventMapper
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.egalacoral.spark.siteserver.model.Event
import spock.lang.Specification

class EventLiveStreamAvailableMapperSpec extends Specification {

  EventLiveStreamAvailableMapper mapper

  EventMapper eventMapper = Mock()

  def setup() {
    eventMapper.map(_, _) >> new EventsModuleData() >> new EventsModuleData()

    mapper = new EventLiveStreamAvailableMapper(eventMapper)
  }

  def "Test Drill Down Tags Names: is Live Steam Available"() {
    expect:

    def moduleDataItem = mapper.map(null, event)
    result == moduleDataItem.isLiveStreamAvailable()

    where:

    event                                                | result
    new Event()                                          | false
    new Event().tap { drilldownTagNames = ' ' }          | false
    new Event().tap { drilldownTagNames = '123' }        | false
    new Event().tap { drilldownTagNames = 'EVFLAG_RVA' } | true
    new Event().tap { drilldownTagNames = 'EVFLAG_PVM' } | true
    new Event().tap { drilldownTagNames = 'EVFLAG_AVA' } | true
    new Event().tap { drilldownTagNames = 'EVFLAG_IVM' } | true
    new Event().tap { drilldownTagNames = 'EVFLAG_RPM' } | true
    new Event().tap { drilldownTagNames = 'EVFLAG_GVM' } | true
  }
}
