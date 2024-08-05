package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.entity.BetReceiptBanner
import com.ladbrokescoral.oxygen.cms.api.repository.BetReceiptBannerExtendedRepository
import com.ladbrokescoral.oxygen.cms.api.service.BetReceiptBannerService

import java.time.Instant
import java.time.LocalDateTime
import java.time.Month
import java.time.ZoneOffset

import spock.lang.Specification

class BetReceiptBannerPublicServiceSpec extends Specification {

  BetReceiptBannerExtendedRepository repository
  BetReceiptBannerPublicService service

  def setup() {
    repository = Mock(BetReceiptBannerExtendedRepository)
    def betReceiptBannerService = new BetReceiptBannerService(null, repository, null, null, null, null)
    service = new BetReceiptBannerPublicService(betReceiptBannerService)
  }

  def "findByBrand returns dto from uninitialized entity"() {
    given:
    def brand = 'bma'

    def entity = new BetReceiptBanner()

    repository.findBetReceiptBanners(brand) >> [entity]

    when:
    def list = service.findByBrand(brand)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.id == null
    dto.name == null
    dto.uriMedium == null
    dto.useDirectFileUrl == null
    dto.directFileUrl == null
    dto.validityPeriodStart == null
    dto.validityPeriodEnd == null
  }

  def "findByBrand returns dto from empty entity"() {
    given:
    def brand = 'connect'

    def entity = new BetReceiptBanner()
    entity.id = ''
    entity.name = ''
    entity.uriMedium = ''
    entity.useDirectFileUrl = false
    entity.directFileUrl = ''
    entity.validityPeriodStart = Instant.EPOCH
    entity.validityPeriodEnd = Instant.EPOCH

    repository.findBetReceiptBanners(brand) >> [entity]

    when:
    def list = service.findByBrand(brand)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.id == entity.id
    dto.name == entity.name
    dto.uriMedium == entity.uriMedium
    dto.useDirectFileUrl == entity.useDirectFileUrl
    dto.directFileUrl == entity.directFileUrl
    dto.validityPeriodStart == '1970-01-01T00:00:00.000Z'
    dto.validityPeriodEnd == '1970-01-01T00:00:00.000Z'
  }

  def "findByBrand"() {
    given:
    def brand = 'ladbrokes'

    def entity = new BetReceiptBanner()
    entity.id = 'ID_Mobile'
    entity.name = 'Bet Receipt Mobile'
    entity.uriMedium = '/images/uploads/medium/640x200.jpg'
    entity.useDirectFileUrl = true
    entity.directFileUrl = 'http://test.com/wp-content/uploads/sports.png'
    entity.validityPeriodStart = LocalDateTime.of(2017, Month.MARCH, 1, 13, 39, 5).toInstant(ZoneOffset.UTC)
    entity.validityPeriodEnd = LocalDateTime.of(2020, Month.MARCH, 1, 13, 39, 6).toInstant(ZoneOffset.UTC)

    repository.findBetReceiptBanners(brand) >> [entity]

    when:
    def list = service.findByBrand(brand)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.id == entity.id
    dto.name == entity.name
    dto.uriMedium == entity.uriMedium
    dto.useDirectFileUrl == entity.useDirectFileUrl
    dto.directFileUrl == entity.directFileUrl
    dto.validityPeriodStart == '2017-03-01T13:39:05.000Z'
    dto.validityPeriodEnd == '2020-03-01T13:39:06.000Z'
  }
}
