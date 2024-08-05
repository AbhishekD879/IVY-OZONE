package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.entity.SsoPage
import com.ladbrokescoral.oxygen.cms.api.repository.SsoPageExtendedRepository
import com.ladbrokescoral.oxygen.cms.api.service.SsoPageService
import spock.lang.Specification

class SsoPagePublicServiceSpec extends Specification {

  SsoPageExtendedRepository repository
  SsoPagePublicService service

  def setup() {
    repository = Mock(SsoPageExtendedRepository)
    def ssoPageService = new SsoPageService(null, repository, null, null, null, null)
    service = new SsoPagePublicService(ssoPageService)
  }

  def "findByBrand returns dto from uninitialized entity"() {
    given:
    def brand = 'bma'
    def osType = 'undefined'

    def entity = new SsoPage()

    repository.findSsoPages(brand, osType) >> [entity]

    when:
    def list = service.findByBrand(brand, osType)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.target == null
    dto.title == null
    dto.uriMedium == null
    dto.openLink == null
  }

  def "findByBrand returns dto from empty entity"() {
    given:
    def brand = 'connect'
    def osType = 'unknown'

    def entity = new SsoPage()
    entity.targetIOS = ''
    entity.targetAndroid = ''
    entity.title = ''
    entity.uriMedium = ''
    entity.openLink = ''

    repository.findSsoPages(brand, osType) >> [entity]

    when:
    def list = service.findByBrand(brand, osType)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.target == null
    dto.title == entity.title
    dto.uriMedium == entity.uriMedium
    dto.openLink == entity.openLink
  }

  def "findByBrand and iOS osType"() {
    given:
    def brand = 'ladbrokes'
    def osType = 'ios'

    def entity = new SsoPage()
    entity.targetIOS = 'com.ios'
    entity.targetAndroid = 'org.android'
    entity.title = 'Casino'
    entity.uriMedium = '/images/uploads/sso-page/medium/160x160.png'
    entity.openLink = '/ios-casino'

    repository.findSsoPages(brand, osType) >> [entity]

    when:
    def list = service.findByBrand(brand, osType)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.target == entity.targetIOS
    dto.title == entity.title
    dto.uriMedium == entity.uriMedium
    dto.openLink == entity.openLink
  }

  def "findByBrand and Android osType"() {
    given:
    def brand = 'rcomb'
    def osType = 'android'

    def entity = new SsoPage()
    entity.targetIOS = 'com.ios'
    entity.targetAndroid = 'org.android'
    entity.title = 'Poker'
    entity.uriMedium = '/images/uploads/sso-page/medium/260x260.png'
    entity.openLink = '/android-poker'

    repository.findSsoPages(brand, osType) >> [entity]

    when:
    def list = service.findByBrand(brand, osType)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.target == entity.targetAndroid
    dto.title == entity.title
    dto.uriMedium == entity.uriMedium
    dto.openLink == entity.openLink
  }
}
