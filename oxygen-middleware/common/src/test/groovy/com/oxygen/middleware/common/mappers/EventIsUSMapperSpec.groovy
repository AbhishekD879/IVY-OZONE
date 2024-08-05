package com.oxygen.middleware.common.mappers

import com.coral.oxygen.middleware.common.mappers.EventIsUSMapper
import com.coral.oxygen.middleware.common.mappers.EventMapper
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.egalacoral.spark.siteserver.model.Event
import spock.lang.Specification

class EventIsUSMapperSpec extends Specification {

  EventIsUSMapper mapper
  EventMapper eventMapper = Mock()

  def setup() {
    eventMapper.map(_, _) >> new EventsModuleData()
    mapper = new EventIsUSMapper(eventMapper)
  }

  def "Test is it US Mapper"() {
    expect:

    def moduleDataItem = mapper.map(null, event)
    result == moduleDataItem.getUS()

    where:

    event                                           | result
    new Event()                                     | false
    new Event().tap { typeFlagCodes = 'UA,EU,US' }  | true
    new Event().tap { typeFlagCodes = 'UA,EU'   }   | false
  }
}
