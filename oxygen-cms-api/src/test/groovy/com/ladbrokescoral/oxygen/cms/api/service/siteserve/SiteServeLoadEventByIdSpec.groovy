package com.ladbrokescoral.oxygen.cms.api.service.siteserve

import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.Children
import com.egalacoral.spark.siteserver.model.Event
import com.egalacoral.spark.siteserver.model.Market

import java.time.Duration
import java.time.Instant

import spock.lang.Specification

class SiteServeLoadEventByIdSpec extends Specification {

  SiteServerApi siteServerApi
  SiteServeApiProvider siteServeApiProvider
  SiteServeLoadEventById siteServeLoadEventById

  def setup() {
    siteServeApiProvider = Mock(SiteServeApiProvider)
    siteServerApi = Mock(SiteServerApi)
    siteServeLoadEventById = new SiteServeLoadEventById("M", "TNMT,TR01", siteServeApiProvider)
    siteServeApiProvider.api("bma") >> siteServerApi
  }

  def "test getting empty eventDto when eventId is unknown"() {
    given:
    def eventId = "111"
    siteServerApi.getEventToOutcomeForEvent(*_) >> Optional.empty()

    when:
    def eventDto = siteServeLoadEventById.loadEvents("bma", eventId, Instant.now(), Instant.now().plus(Duration.ofDays(1)))

    then:
    Objects.nonNull(eventDto)
    eventDto.isEmpty()
  }

  def "test getting valid eventDto by eventId"() {
    given:
    def eventId = "1"
    siteServerApi.getEventToOutcomeForEvent(*_) >> Optional.of(Collections.singletonList(createEvent(eventId)))

    when:
    def eventDto = siteServeLoadEventById.loadEvents("bma", eventId, Instant.now(), Instant.now().plus(Duration.ofDays(1)))

    then:
    Objects.nonNull(eventDto)
    eventDto.size() == 1
    eventDto.get(0).getId() == eventId
    !eventDto.get(0).isOutright()
  }

  def "test getting valid eventDto by outright eventId"() {
    given:
    def eventId = "1"
    siteServerApi.getEventToOutcomeForEvent(*_) >> Optional.of(Collections.singletonList(createOutrightEvent(eventId)))

    when:
    def eventDto = siteServeLoadEventById.loadEvents("bma", eventId, Instant.now(), Instant.now().plus(Duration.ofDays(1)))

    then:
    Objects.nonNull(eventDto)
    eventDto.size() == 1
    eventDto.get(0).getId() == eventId
    eventDto.get(0).getNameOverride() == "Test event"
    eventDto.get(0).isOutright()
  }

  Event createEvent(String eventId) {
    def market = new Market()
    market.id = "market1"
    def eventChildren = new Children()
    eventChildren.market = market
    def event = new Event()
    event.id = eventId
    event.name = "Test event"
    event.isActive = true
    event.children = Collections.singletonList(eventChildren)
    event.isAvailable = true
    event.siteChannels = "P,Q,C,I"
    event.eventSortCode = "MTCH"
    event
  }

  Event createOutrightEvent(String eventId) {
    Event event = createEvent(eventId)
    event.siteChannels = "P,Q,C,I,M"
    event.eventSortCode = "TNMT"
    event
  }
}
