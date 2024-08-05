package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.entity.BetReceiptBannerTablet
import com.ladbrokescoral.oxygen.cms.api.repository.BetReceiptBannerExtendedRepository
import com.ladbrokescoral.oxygen.cms.api.service.BetReceiptBannerTabletService

import java.time.Instant
import java.time.LocalDateTime
import java.time.Month
import java.time.ZoneOffset

import spock.lang.Specification

class BetReceiptBannerTabletPublicServiceSpec extends Specification {

  BetReceiptBannerExtendedRepository repository
  BetReceiptBannerTabletPublicService service

  def setup() {
    repository = Mock(BetReceiptBannerExtendedRepository)
    def betReceiptBannerTabletService = new BetReceiptBannerTabletService(null, repository, null, null, null, null)
    service = new BetReceiptBannerTabletPublicService(betReceiptBannerTabletService)
  }

  def "findByBrand returns dto from uninitialized entity"() {
    given:
    def brand = 'bma'

    def entity = new BetReceiptBannerTablet()

    repository.findBetReceiptBanners(brand) >> [entity]

    when:
    def list = service.findByBrand(brand)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.id == null
    dto.name == null
    dto.uriMedium == null
    dto.validityPeriodStart == null
    dto.validityPeriodEnd == null
  }

  def "findByBrand returns dto from empty entity"() {
    given:
    def brand = 'connect'

    def entity = new BetReceiptBannerTablet()
    entity.id = ''
    entity.name = ''
    entity.uriMedium = ''
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
    dto.validityPeriodStart == '1970-01-01T00:00:00.000Z'
    dto.validityPeriodEnd == '1970-01-01T00:00:00.000Z'
  }

  def "findByBrand"() {
    given:
    def brand = 'ladbrokes'

    def entity = new BetReceiptBannerTablet()
    entity.id = 'ID_Tablet'
    entity.name = 'Bet Receipt Tablet'
    entity.uriMedium = '/images/uploads/betReceiptBannersTablet/medium/720x170.png'
    entity.validityPeriodStart = LocalDateTime.of(2016, Month.DECEMBER, 29, 10, 21, 51).toInstant(ZoneOffset.UTC)
    entity.validityPeriodEnd = LocalDateTime.of(2027, Month.FEBRUARY, 17, 10, 21, 52).toInstant(ZoneOffset.UTC)

    repository.findBetReceiptBanners(brand) >> [entity]

    when:
    def list = service.findByBrand(brand)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.id == entity.id
    dto.name == entity.name
    dto.uriMedium == entity.uriMedium
    dto.validityPeriodStart == '2016-12-29T10:21:51.000Z'
    dto.validityPeriodEnd == '2027-02-17T10:21:52.000Z'
  }
}
