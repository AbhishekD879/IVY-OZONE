package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.entity.SimpleModule
import com.ladbrokescoral.oxygen.cms.api.entity.SportsFeaturedTab
import com.ladbrokescoral.oxygen.cms.api.repository.SportsFeaturedTabRepository
import com.ladbrokescoral.oxygen.cms.api.service.SportsFeaturedTabService
import spock.lang.Specification

class SportsFeaturedTabPublicServiceSpec extends Specification {

  final PATH = 'default path'

  SportsFeaturedTabRepository repository
  SportsFeaturedTabPublicService service

  def setup() {
    repository = Mock(SportsFeaturedTabRepository)
    def sportsFeaturedTabService = new SportsFeaturedTabService(repository)
    service = new SportsFeaturedTabPublicService(sportsFeaturedTabService)
  }

  def "getFeatureTabByPath returns dto from uninitialized entity"() {
    given:
    def brand = 'bma'

    def entity = new SportsFeaturedTab()

    repository.findByBrandIgnoreCaseAndPathIgnoreCaseAndDisabledIsFalse(brand, PATH) >> entity

    when:
    def tab = service.getFeatureTabByPath(brand, PATH)

    then:
    def dto = tab.get()
    dto.name == null
    dto.categoryId == null
    dto.modules.empty
  }

  def "getFeatureTabByPath returns dto from empty entity"() {
    given:
    def brand = 'connect'

    def moduleEntity = new SimpleModule()
    moduleEntity.originalName = ''
    moduleEntity.displayName = ''
    moduleEntity.description = ''
    moduleEntity.displayOrder = 0
    moduleEntity.disabled = false

    def entity = new SportsFeaturedTab()
    entity.name = ''
    entity.categoryId = ''
    entity.modules = [moduleEntity]

    repository.findByBrandIgnoreCaseAndPathIgnoreCaseAndDisabledIsFalse(brand, PATH) >> entity

    when:
    def tab = service.getFeatureTabByPath(brand, PATH)

    then:
    def dto = tab.get()
    dto.name == entity.name
    dto.categoryId == entity.categoryId
    dto.modules.size() == 1

    def moduleDto = dto.modules.get 0
    moduleDto.originalName == moduleEntity.originalName
    moduleDto.displayName == moduleEntity.displayName
    moduleDto.description == moduleEntity.description
    moduleDto.displayOrder == moduleEntity.displayOrder
  }

  def "getFeatureTabByPath"() {
    given:
    def brand = 'ladbrokes'

    def moduleEntity = new SimpleModule()
    moduleEntity.originalName = 'football-live'
    moduleEntity.displayName = 'Football'
    moduleEntity.description = 'Football live events'
    moduleEntity.displayOrder = 2
    moduleEntity.disabled = true

    def entity = new SportsFeaturedTab()
    entity.name = 'Live'
    entity.categoryId = 'live-1'
    entity.modules = [moduleEntity]

    repository.findByBrandIgnoreCaseAndPathIgnoreCaseAndDisabledIsFalse(brand, PATH) >> entity

    when:
    def tab = service.getFeatureTabByPath(brand, PATH)

    then:
    def dto = tab.get()
    dto.name == entity.name
    dto.categoryId == entity.categoryId
    dto.modules.size() == 1

    def moduleDto = dto.modules.get 0
    moduleDto.originalName == moduleEntity.originalName
    moduleDto.displayName == moduleEntity.displayName
    moduleDto.description == moduleEntity.description
    moduleDto.displayOrder == moduleEntity.displayOrder
  }
}
