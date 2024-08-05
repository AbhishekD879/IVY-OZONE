package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.TestUtil
import com.ladbrokescoral.oxygen.cms.api.dto.SportCategoryDto
import com.ladbrokescoral.oxygen.cms.api.entity.Filename
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository
import com.ladbrokescoral.oxygen.cms.api.repository.SportTabRepository
import com.ladbrokescoral.oxygen.cms.api.service.InplayStatsDisplayService
import com.ladbrokescoral.oxygen.cms.api.service.InplayStatsSortingService
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService
import spock.lang.Specification

class SportCategoryPublicServiceSpec extends Specification {

  SportCategoryRepository categoryRepository
  SportTabRepository tabRepository
  SegmentService segmentService;
  InplayStatsDisplayService statsDisplayService
  InplayStatsSortingService statsSortingService
  SportCategoryPublicService service

  def setup() {
    categoryRepository = Mock(SportCategoryRepository)
    segmentService=Mock(SegmentService)
    statsDisplayService = Mock(InplayStatsDisplayService)
    statsSortingService = Mock(InplayStatsSortingService)
    service = new SportCategoryPublicService(categoryRepository, tabRepository,segmentService,statsDisplayService,statsSortingService)
  }

  def "cms api return right sport category public structure"() {
    given:
    def brand = "bma"
    def disabled = false
    categoryRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand,disabled) >> TestUtil.deserializeListWithJackson("service/public_api/full_sport_category.json", SportCategory.class)

    when:
    def result = service.findByBrand(brand)
    SportCategoryDto sportCategoryDto = (SportCategoryDto) result.get(0)

    then:
    !sportCategoryDto.disabled
  }

  def "findNative returns dto from uninitialized entity"() {
    given:
    def brand = 'connect'
    def disabled = false

    def entity = new SportCategory()

    categoryRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand,disabled) >> [entity]

    when:
    def list = service.findNative(brand)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.id == null
    dto.filename == null
    dto.uriLarge == ''
    dto.uriMedium == ''
    dto.uriSmall == ''
    dto.widthLarge == null
    dto.widthMedium == null
    dto.widthSmall == null
    dto.heightLarge == null
    dto.heightMedium == null
    dto.heightSmall == null
    dto.uriLargeIcon == ''
    dto.uriMediumIcon == ''
    dto.uriSmallIcon == ''
    dto.alt == null
    dto.imageTitle == null
    dto.categoryId == null
    dto.ssCategoryCode == ''
    dto.targetUri == null
    !dto.disabled
    !dto.showInPlay
    !dto.showInHome
    !dto.showInAZ
    dto.path == null
    dto.isTopSport == null
    !dto.inApp
    !dto.showScoreboard
    dto.scoreBoardUrl == null
    !dto.hasEvents
  }

  def "findNative returns dto from empty entity"() {
    given:
    def brand = 'rcomb'
    def disabled = false


    def entity = new SportCategory()
    entity.id = ''
    entity.filename = new Filename()
    entity.uriLarge = ''
    entity.uriMedium = ''
    entity.uriSmall = ''
    entity.widthLarge = 0
    entity.widthMedium = 0
    entity.widthSmall = 0
    entity.heightLarge = 0
    entity.heightMedium = 0
    entity.heightSmall = 0
    entity.uriLargeIcon = ''
    entity.uriMediumIcon = ''
    entity.uriSmallIcon = ''
    entity.alt = ''
    entity.imageTitle = ''
    entity.categoryId = 0
    entity.ssCategoryCode = ''
    entity.targetUri = ''
    entity.disabled = false
    entity.showInPlay = false
    entity.showInHome = false
    entity.showInAZ = false
    entity.path = ''
    entity.isTopSport = false
    entity.inApp = false
    entity.showScoreboard = false
    entity.scoreBoardUri = ''
    entity.hasEvents = false

    categoryRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand,disabled) >> [entity]

    when:
    def list = service.findNative(brand)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.id == entity.id
    dto.filename == null
    dto.uriLarge == entity.uriLarge
    dto.uriMedium == entity.uriMedium
    dto.uriSmall == entity.uriSmall
    dto.widthLarge == entity.widthLarge
    dto.widthMedium == entity.widthMedium
    dto.widthSmall == entity.widthSmall
    dto.heightLarge == entity.heightLarge
    dto.heightMedium == entity.heightMedium
    dto.heightSmall == entity.heightSmall
    dto.uriLargeIcon == entity.uriLargeIcon
    dto.uriMediumIcon == entity.uriMediumIcon
    dto.uriSmallIcon == entity.uriSmallIcon
    dto.alt == entity.alt
    dto.imageTitle == entity.imageTitle
    dto.categoryId == entity.categoryId
    dto.ssCategoryCode == entity.ssCategoryCode
    dto.targetUri == entity.targetUri
    dto.disabled == entity.disabled
    dto.showInPlay == entity.showInPlay
    dto.showInHome == entity.showInHome
    dto.showInAZ == entity.showInAZ
    dto.path == entity.path
    dto.isTopSport == entity.isTopSport
    dto.inApp == entity.inApp
    dto.showScoreboard == entity.showScoreboard
    dto.scoreBoardUrl == entity.scoreBoardUri
    dto.hasEvents == entity.hasEvents
  }

  def "find by brand excludes 'public' form uri if it appears at the beginning of the string"() {
    given:
    def brand = 'secondscreen'
    def disabled = false

    def entity = new SportCategory()
    entity.uriLarge = 'public/large-public'
    entity.uriMedium = 'public/medium-public'
    entity.uriSmall = 'public/small-public'
    entity.uriLargeIcon = 'public/large-public-icon'
    entity.uriMediumIcon = 'public/medium-public-icon'
    entity.uriSmallIcon = 'public/small-public-icon'

    categoryRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand,disabled) >> [entity]

    when:
    def list = service.findNative(brand)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.uriLarge == '/large-public'
    dto.uriMedium == '/medium-public'
    dto.uriSmall == '/small-public'
    dto.uriLargeIcon == '/large-public-icon'
    dto.uriMediumIcon == '/medium-public-icon'
    dto.uriSmallIcon == '/small-public-icon'
  }

  def "findNative"() {
    given:
    def brand = 'ladbrokes'
    def disabled = false

    def filename = new Filename()
    filename.filename = 'file.txt'

    def entity = new SportCategory()
    entity.id = 'ID'
    entity.filename = filename
    entity.uriLarge = '/large.png'
    entity.uriMedium = '/medium.png'
    entity.uriSmall = '/small.png'
    entity.widthLarge = 64
    entity.widthMedium = 32
    entity.widthSmall = 16
    entity.heightLarge = 40
    entity.heightMedium = 30
    entity.heightSmall = 20
    entity.uriLargeIcon = '/icon-large.png'
    entity.uriMediumIcon = '/icon-medium.png'
    entity.uriSmallIcon = '/icon-small.png'
    entity.alt = 'tennis'
    entity.imageTitle = 'Tennis'
    entity.categoryId = 999
    entity.ssCategoryCode = 'TENNIS'
    entity.targetUri = 'sport/tennis'
    entity.disabled = true
    entity.showInPlay = true
    entity.showInHome = true
    entity.showInAZ = true
    entity.path = '/tennis'
    entity.isTopSport = true
    entity.inApp = true
    entity.showScoreboard = true
    entity.scoreBoardUri = '/tennis-scoreboard'
    entity.hasEvents = true

    categoryRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand,disabled) >> [entity]

    when:
    def list = service.findNative(brand)

    then:
    list.size() == 1

    def dto = list.get 0
    dto.id == entity.id
    dto.filename == entity.filename.filename
    dto.uriLarge == entity.uriLarge
    dto.uriMedium == entity.uriMedium
    dto.uriSmall == entity.uriSmall
    dto.widthLarge == entity.widthLarge
    dto.widthMedium == entity.widthMedium
    dto.widthSmall == entity.widthSmall
    dto.heightLarge == entity.heightLarge
    dto.heightMedium == entity.heightMedium
    dto.heightSmall == entity.heightSmall
    dto.uriLargeIcon == entity.uriLargeIcon
    dto.uriMediumIcon == entity.uriMediumIcon
    dto.uriSmallIcon == entity.uriSmallIcon
    dto.alt == entity.alt
    dto.imageTitle == entity.imageTitle
    dto.categoryId == entity.categoryId
    dto.ssCategoryCode == entity.ssCategoryCode
    dto.targetUri == entity.targetUri
    dto.disabled == entity.disabled
    dto.showInPlay == entity.showInPlay
    dto.showInHome == entity.showInHome
    dto.showInAZ == entity.showInAZ
    dto.path == entity.path
    dto.isTopSport == entity.isTopSport
    dto.inApp == entity.inApp
    dto.showScoreboard == entity.showScoreboard
    dto.scoreBoardUrl == entity.scoreBoardUri
    dto.hasEvents == entity.hasEvents
  }
}
