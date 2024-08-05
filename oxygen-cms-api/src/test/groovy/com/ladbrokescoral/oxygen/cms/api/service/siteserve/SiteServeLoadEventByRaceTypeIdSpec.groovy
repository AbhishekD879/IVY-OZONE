package com.ladbrokescoral.oxygen.cms.api.service.siteserve

import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.Children
import com.egalacoral.spark.siteserver.model.Event
import com.egalacoral.spark.siteserver.model.Market
import com.ladbrokescoral.oxygen.cms.configuration.MarketTemplateFilterConfig

import java.time.Duration
import java.time.Instant

import spock.lang.Specification

class SiteServeLoadEventByRaceTypeIdSpec extends Specification {

  SiteServerApi siteServerApi
  SiteServeApiProvider siteServeApiProvider
  SiteServeLoadEventByRaceTypeId siteServeLoadEventByRaceTypeId
  MarketTemplateFilterConfig marketTemplateFilterConfig

  def setup() {
    siteServeApiProvider = Mock(SiteServeApiProvider)
    siteServerApi = Mock(SiteServerApi)
    marketTemplateFilterConfig = new MarketTemplateFilterConfig()
    marketTemplateFilterConfig.setRaceTypeTemplateNames(new HashMap<String, String>())

    siteServeLoadEventByRaceTypeId = new SiteServeLoadEventByRaceTypeId(siteServeApiProvider, marketTemplateFilterConfig)
    siteServeApiProvider.api("bma") >> siteServerApi
  }

  def "test getting empty eventDto when raceTypeId is unknown"() {
    given:
    def raceTypeId = "111"
    siteServerApi.getEventToOutcomeForType(*_) >> Optional.empty()

    when:
    def eventDto = siteServeLoadEventByRaceTypeId.loadEvents("bma", raceTypeId, Instant.now(), Instant.now().plus(Duration.ofDays(1)))

    then:
    Objects.nonNull(eventDto)
    eventDto.isEmpty()
  }

  def "test getting valid eventDto by raceTypeId"() {
    given:
    def raceTypeId = "1"
    siteServerApi.getEventToOutcomeForType(*_) >> Optional.of(Collections.singletonList(createEvent(raceTypeId)))

    when:
    def eventDto = siteServeLoadEventByRaceTypeId.loadEvents("bma", raceTypeId, Instant.now(), Instant.now().plus(Duration.ofDays(1)))

    then:
    Objects.nonNull(eventDto)
    eventDto.size() == 1
    eventDto.get(0).getId() == raceTypeId
  }

  def "test skipping eventDto without children"() {
    given:
    def raceTypeId = "1"
    def event = createEvent(raceTypeId)
    event.children = Collections.emptyList()
    siteServerApi.getEventToOutcomeForType(*_) >> Optional.of(Collections.singletonList(event))

    when:
    def eventDto = siteServeLoadEventByRaceTypeId.loadEvents("bma", raceTypeId, Instant.now(), Instant.now().plus(Duration.ofDays(1)))

    then:
    Objects.nonNull(eventDto)
    eventDto.size() == 0
  }

  def "test getting eventDto with LiveServChildrenChannels"() {
    given:
    def raceTypeId = "1"
    def event = createEvent(raceTypeId)
    event.liveServChildrenChannels = "12345"
    siteServerApi.getEventToOutcomeForType(*_) >> Optional.of(Collections.singletonList(event))

    when:
    def eventDto = siteServeLoadEventByRaceTypeId.loadEvents("bma", raceTypeId, Instant.now(), Instant.now().plus(Duration.ofDays(1)))

    then:
    Objects.nonNull(eventDto)
    eventDto.size() == 1
    eventDto.get(0).getId() == raceTypeId
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
    event
  }
}
