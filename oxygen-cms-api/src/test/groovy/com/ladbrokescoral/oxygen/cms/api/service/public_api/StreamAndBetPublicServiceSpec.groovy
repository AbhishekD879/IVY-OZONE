package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.entity.StreamAndBet
import com.ladbrokescoral.oxygen.cms.api.repository.StreamAndBetRepository
import com.ladbrokescoral.oxygen.cms.api.service.StreamAndBetService
import spock.lang.Specification

class StreamAndBetPublicServiceSpec extends Specification {

  StreamAndBetRepository repository
  StreamAndBetPublicService service

  def setup() {
    repository = Mock(StreamAndBetRepository)
    def streamAndBetService = new StreamAndBetService(repository)
    service = new StreamAndBetPublicService(streamAndBetService)
  }

  def "findByBrand does not return dto from uninitialized entity"() {
    given:
    def brand = 'connect'

    def entity = new StreamAndBet()

    repository.findOneByBrand(brand) >> new Optional(entity)

    when:
    def optionalList = service.findByBrand(brand)

    then:
    !optionalList.present
  }

  def "findByBrand does not return dto from entity with no children"() {
    given:
    def brand = 'bma'

    def entity = new StreamAndBet()
    entity.brand = brand
    entity.children = []

    repository.findOneByBrand(brand) >> new Optional(entity)

    when:
    def optionalList = service.findByBrand(brand)

    then:
    optionalList.present
    optionalList.get().empty
  }

  def "findByBrand returns dto from uninitialized child entity"() {
    given:
    def brand = 'secondscreen'

    def childEntity = new StreamAndBet.SABChildElement()

    def entity = new StreamAndBet()
    entity.brand = brand
    entity.children = [childEntity]

    repository.findOneByBrand(brand) >> new Optional(entity)

    when:
    def optionalList = service.findByBrand(brand)

    then:
    optionalList.present

    def list = optionalList.get()
    list.size() == 1

    def childDto = list.get 0
    childDto.id == null
    childDto.name == null
    !childDto.androidActive
    !childDto.iosActive
    childDto.children == null
  }

  def "findByBrand returns dto from empty child entity"() {
    given:
    def brand = 'rcomb'

    def childEntity = new StreamAndBet.SABChildElement()
    childEntity.siteServeId = 0
    childEntity.name = ''
    childEntity.showItemFor = ''
    childEntity.selection = ''
    childEntity.children = []

    def entity = new StreamAndBet()
    entity.brand = brand
    entity.children = [childEntity]

    repository.findOneByBrand(brand) >> new Optional(entity)

    when:
    def optionalList = service.findByBrand(brand)

    then:
    optionalList.present

    def list = optionalList.get()
    list.size() == 1

    def childDto = list.get 0
    childDto.id == childEntity.siteServeId
    childDto.name == childEntity.name
    !childDto.androidActive
    !childDto.iosActive
    childDto.children.empty
  }

  def "findByBrand"() {
    given:
    def brand = 'ladbrokes'

    def firstSubChildEntity = new StreamAndBet.SABChildElement()
    firstSubChildEntity.siteServeId = 6
    firstSubChildEntity.name = 'sub name 1'
    firstSubChildEntity.showItemFor = 'ios'
    firstSubChildEntity.selection = 'last'
    firstSubChildEntity.children = []

    def secondSubChildEntity = new StreamAndBet.SABChildElement()
    secondSubChildEntity.siteServeId = 7
    secondSubChildEntity.name = 'sub name 2'
    secondSubChildEntity.showItemFor = 'android'
    secondSubChildEntity.selection = 'first'
    secondSubChildEntity.children = []

    def childEntity = new StreamAndBet.SABChildElement()
    childEntity.siteServeId = 5
    childEntity.name = 'name 1'
    childEntity.showItemFor = 'both'
    childEntity.selection = 'all'
    childEntity.children = [
      firstSubChildEntity,
      secondSubChildEntity
    ]

    def rootEntity = new StreamAndBet()
    rootEntity.brand = brand
    rootEntity.children = [childEntity]

    repository.findOneByBrand(brand) >> new Optional(rootEntity)

    when:
    def optionalList = service.findByBrand(brand)

    then:
    optionalList.present

    def list = optionalList.get()
    list.size() == 1

    def childDto = list.get 0
    childDto.id == childEntity.siteServeId
    childDto.name == childEntity.name
    childDto.androidActive
    childDto.iosActive
    childDto.children.size() == 2

    def firstSubChildDto = childDto.children.get 0
    firstSubChildDto.id == firstSubChildEntity.siteServeId
    firstSubChildDto.name == firstSubChildEntity.name
    !firstSubChildDto.androidActive
    firstSubChildDto.iosActive
    firstSubChildDto.children.empty

    def secondSubChildDto = childDto.children.get 1
    secondSubChildDto.id == secondSubChildEntity.siteServeId
    secondSubChildDto.name == secondSubChildEntity.name
    secondSubChildDto.androidActive
    !secondSubChildDto.iosActive
    secondSubChildDto.children.empty
  }
}
