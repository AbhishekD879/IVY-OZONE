package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.entity.QuickLink
import com.ladbrokescoral.oxygen.cms.api.repository.QuickLinkExtendedRepository
import com.ladbrokescoral.oxygen.cms.api.service.QuickLinkService

import java.time.Instant
import java.time.LocalDateTime
import java.time.Month
import java.time.ZoneOffset

import spock.lang.Specification

class QuickLinkPublicServiceSpec extends Specification {

  final RACE_TYPE = 'horseracing'

  QuickLinkExtendedRepository repository
  QuickLinkPublicService service

  def setup() {
    repository = Mock(QuickLinkExtendedRepository)
    def quickLinkService = new QuickLinkService(null, repository)
    service = new QuickLinkPublicService(quickLinkService)
  }

  def "findByBrand returns dto from uninitialized entity"() {
    given:
    def brand = 'bma'

    def entity = new QuickLink()

    repository.findQuickLinks(brand, RACE_TYPE) >> [entity]

    when:
    def list = service.findByBrand(brand, RACE_TYPE)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.title == null
    dto.body == null
    dto.linkType == null
    dto.target == null
    dto.raceType == null
    dto.validityPeriodStart == null
    dto.validityPeriodEnd == null
    dto.iconUrl == null
    dto.iconLargeUrl == null
  }

  def "findByBrand returns dto from empty entity"() {
    given:
    def brand = 'connect'

    def entity = new QuickLink()
    entity.title = ''
    entity.body = ''
    entity.linkType = ''
    entity.target = ''
    entity.raceType = ''
    entity.validityPeriodStart = Instant.EPOCH
    entity.validityPeriodEnd = Instant.EPOCH
    entity.uriLarge = ''
    entity.uriMedium = ''

    repository.findQuickLinks(brand, RACE_TYPE) >> [entity]

    when:
    def list = service.findByBrand(brand, RACE_TYPE)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.title == entity.title
    dto.body == entity.body
    dto.linkType == entity.linkType
    dto.target == entity.target
    dto.raceType == entity.raceType
    dto.validityPeriodStart == '1970-01-01T00:00:00.000Z'
    dto.validityPeriodEnd == '1970-01-01T00:00:00.000Z'
    dto.iconLargeUrl == entity.uriLarge
    dto.iconUrl == entity.uriMedium
  }

  def "findByBrand"() {
    given:
    def brand = 'ladbrokes'

    def entity = new QuickLink()
    entity.title = 'Horse link'
    entity.body = 'test'
    entity.linkType = 'url'
    entity.target = 'lotto'
    entity.raceType = RACE_TYPE
    entity.validityPeriodStart = LocalDateTime.of(2018, Month.DECEMBER, 31, 23, 59, 59).toInstant(ZoneOffset.UTC)
    entity.validityPeriodEnd = LocalDateTime.of(2019, Month.JANUARY, 1, 0, 0, 0).toInstant(ZoneOffset.UTC)
    entity.uriLarge = '/large.png'
    entity.uriMedium = '/medium.png'

    repository.findQuickLinks(brand, RACE_TYPE) >> [entity]

    when:
    def list = service.findByBrand(brand, RACE_TYPE)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.title == entity.title
    dto.body == entity.body
    dto.linkType == entity.linkType
    dto.target == entity.target
    dto.raceType == entity.raceType
    dto.validityPeriodStart == '2018-12-31T23:59:59.000Z'
    dto.validityPeriodEnd == '2019-01-01T00:00:00.000Z'
    dto.iconLargeUrl == entity.uriLarge
    dto.iconUrl == entity.uriMedium
  }
}
