package com.coral.oxygen.edp.tracking.virtuals

import com.coral.oxygen.edp.model.mapping.EventMapper
import com.coral.oxygen.edp.model.output.OutputEvent
import com.egalacoral.spark.siteserver.api.ExistsFilter
import com.egalacoral.spark.siteserver.api.SimpleFilter
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.api.SiteServerImpl
import com.egalacoral.spark.siteserver.model.Children
import com.egalacoral.spark.siteserver.model.Event
import spock.lang.Specification
import com.egalacoral.spark.siteserver.parameter.RacingForm
import java.util.EnumSet

import static com.coral.oxygen.edp.TestUtil.*

class VirtualMarketsDataConsumerSpec extends Specification {

  def MOCK_EVENT_ID = 11899739L
  def MOCK_EVENT_ID_INVALID = 100L
  def QUEUE_SIZE = 5
  def THREADS_COUNT = 3
  SiteServerApi siteServerApiStub
  EventMapper eventMapperMock
  OutputEvent mockOutputEvent = deserializeWithJackson("/virtuals/event_virtual_mapped.json", OutputEvent.class)

  List<Children> mockEvent = deserializeListWithJackson("/virtuals/event_virtual_children.json", Children.class)

  VirtualMarketsDataConsumer virtualMarketsDataConsumer

  def setup() {
    eventMapperMock = Mock(EventMapper) {
      map(_ as OutputEvent, _ as Event) >> mockOutputEvent
    }
    siteServerApiStub = Stub(SiteServerApi)

    siteServerApiStub.getEventToOutcomeForEvent(
        Collections.singletonList(String.valueOf(MOCK_EVENT_ID)),
        SiteServerImpl.EMPTY_SIMPLE_FILTER,
        EnumSet.of(RacingForm.OUTCOME),
        null,
        false) >> Optional.of(mockEvent)

    virtualMarketsDataConsumer = new VirtualMarketsDataConsumer(
        siteServerApiStub,
        QUEUE_SIZE,
        THREADS_COUNT,
        eventMapperMock)
  }

  def "Test consumer interaction for valid id"() {
    given: 'Prepare event id Set'

    def idSet = new HashSet<Long>()
    idSet.add(MOCK_EVENT_ID)

    when: 'Call consumers #doConsume()'
    def result = virtualMarketsDataConsumer.doConsume(idSet)

    then: 'Consumer returns the map with id as a key, and Event as a value'
    result.get(MOCK_EVENT_ID).getEvent() == mockOutputEvent
  }

  def "Test consumer return empty Map if event id is invalid"() {
    given: 'Prepare id Set'
    def ids = new HashSet<Long>()
    ids.add(MOCK_EVENT_ID_INVALID)

    when: 'Consumer receives #doConsume call'
    def result = virtualMarketsDataConsumer.doConsume(ids)

    then: 'Consumer returns empty map'
    result == Collections.emptyMap()
  }
}
