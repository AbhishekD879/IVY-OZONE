package com.oxygen.middleware.common.mappers

import com.coral.oxygen.middleware.common.mappers.EventMapper
import com.coral.oxygen.middleware.common.mappers.EventTypeFlagCodesMapper
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.egalacoral.spark.siteserver.model.Event
import spock.lang.Specification

class EventTypeFlagCodesMapperSpec extends Specification {

  EventTypeFlagCodesMapper mapper
  EventMapper chain = Mock()

  def "Test is live stream returns type flag code"() {
    setup:
    chain.map(_, _) >> moduleItem
    mapper = new EventTypeFlagCodesMapper(chain)

    expect:
    def expectedModuleDataItem = mapper.map(moduleItem, event)
    resultLiveStreamTypeFlagCode == expectedModuleDataItem.getTypeFlagCodes()

    where:
    moduleItem                              | event                                      | resultLiveStreamTypeFlagCode
    new EventsModuleData()                  | new Event()                                | null
    new EventsModuleData().tap
        { liveStreamAvailable = Boolean.FALSE } | new Event()                                | null
    new EventsModuleData().tap
        { liveStreamAvailable = Boolean.TRUE }  | new Event()                                | null
    new EventsModuleData().tap
        { liveStreamAvailable = Boolean.TRUE }  | new Event().tap { typeFlagCodes = 'IVA,' } | 'IVA,'
  }
}
