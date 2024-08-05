package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.entity.EdpMarket
import com.ladbrokescoral.oxygen.cms.api.repository.EdpMarketRepository
import com.ladbrokescoral.oxygen.cms.api.service.EdpMarketService
import spock.lang.Specification

class EdpMarketPublicServiceSpec extends Specification {

  EdpMarketRepository repository
  EdpMarketPublicService service

  def setup() {
    repository = Mock(EdpMarketRepository)
    def edpMarketService = new EdpMarketService(repository)
    service = new EdpMarketPublicService(edpMarketService)
  }

  def "findByBrand returns dto from uninitialized entity"() {
    given:
    def brand = 'bma'

    def entity = new EdpMarket()

    repository.findAllByBrandOrderBySortOrderAsc(brand) >> [entity]

    when:
    def list = service.findByBrand(brand)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.id == null
    dto.name == null
    dto.marketId == null
    !dto.lastItem
  }

  def "findByBrand returns dto from empty entity"() {
    given:
    def brand = 'connect'

    def entity = new EdpMarket()
    entity.id = ''
    entity.name = ''
    entity.marketId = ''
    entity.lastItem = false

    repository.findAllByBrandOrderBySortOrderAsc(brand) >> [entity]

    when:
    def list = service.findByBrand(brand)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.id == entity.id
    dto.name == entity.name
    dto.marketId == entity.marketId
    dto.lastItem == entity.lastItem
  }

  def "findByBrand"() {
    given:
    def brand = 'ladbrokes'

    def entity = new EdpMarket()
    entity.id = 'ID'
    entity.name = 'Market'
    entity.marketId = 'm1'
    entity.lastItem = true

    repository.findAllByBrandOrderBySortOrderAsc(brand) >> [entity]

    when:
    def list = service.findByBrand(brand)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.id == entity.id
    dto.name == entity.name
    dto.marketId == entity.marketId
    dto.lastItem == entity.lastItem
  }
}
