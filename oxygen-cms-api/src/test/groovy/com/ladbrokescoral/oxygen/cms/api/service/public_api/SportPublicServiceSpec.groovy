package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.entity.Filename
import com.ladbrokescoral.oxygen.cms.api.entity.Sport
import com.ladbrokescoral.oxygen.cms.api.entity.Tab
import com.ladbrokescoral.oxygen.cms.api.repository.SportRepository
import spock.lang.Specification

class SportPublicServiceSpec extends Specification {

  final VIEW_BY_FILTERS = Collections.unmodifiableList(["byCompetitions", "byTime"])

  SportRepository repository
  SportPublicService service

  def setup() {
    repository = Mock(SportRepository)
    service = new SportPublicService(repository)
  }

  def "find by brand returns dto from uninitialized entity"() {
    given:
    def brand = 'bma'
    def disabled = false

    def entity = new Sport()

    repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand,disabled) >> [entity]

    when:
    def list = service.find(brand)

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
    dto.svg == null
    dto.svgId == null
    dto.alt == null
    dto.imageTitle == null
    dto.categoryId == null
    dto.typeIds.empty
    dto.ssCategoryCode == ''
    dto.targetUri == null
    dto.dispSortName.empty
    dto.primaryMarkets == null
    dto.viewByFilters.size() == 2
    dto.viewByFilters == VIEW_BY_FILTERS
    dto.oddsCardHeaderType != null
    dto.oddsCardHeaderType.outcomesTemplateType1 == null
    dto.oddsCardHeaderType.outcomesTemplateType2 == null
    dto.oddsCardHeaderType.outcomesTemplateType3 == null
    !dto.disabled
    dto.showInPlay == null
    dto.isOutrightSport == null
    dto.isMultiTemplateSport == null
    dto.tabs != null
    dto.tabs.tabLive == null
    dto.tabs.tabMatches == null
    dto.tabs.tabOutrights == null
    dto.tabs.tabSpecials == null
    dto.defaultTab == null
    dto.inApp == null
  }

  def "find by brand returns dto from empty entity"() {
    given:
    def brand = 'connect'
    def disabled = false

    def entity = new Sport()
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
    entity.svg = ''
    entity.svgId = ''
    entity.alt = ''
    entity.imageTitle = ''
    entity.categoryId = 0
    entity.typeIds = ''
    entity.ssCategoryCode = ''
    entity.targetUri = ''
    entity.dispSortName = ''
    entity.primaryMarkets = ''
    entity.viewByFilters = ''
    entity.outcomesTemplateType1 = ''
    entity.outcomesTemplateType2 = ''
    entity.outcomesTemplateType3 = ''
    entity.disabled = false
    entity.showInPlay = false
    entity.isOutrightSport = false
    entity.isMultiTemplateSport = false
    entity.tabLive = new Tab()
    entity.tabMatches = new Tab()
    entity.tabOutrights = new Tab()
    entity.tabSpecials = new Tab()
    entity.defaultTab = ''
    entity.inApp = false

    repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand,disabled) >> [entity]

    when:
    def list = service.find(brand)

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
    dto.svg == entity.svg
    dto.svgId == entity.svgId
    dto.alt == entity.alt
    dto.imageTitle == entity.imageTitle
    dto.categoryId == entity.categoryId.toString()
    dto.typeIds.empty
    dto.ssCategoryCode == entity.ssCategoryCode
    dto.targetUri == entity.targetUri
    dto.dispSortName.empty
    dto.primaryMarkets == entity.primaryMarkets
    dto.viewByFilters.size() == 2
    dto.viewByFilters == VIEW_BY_FILTERS
    dto.oddsCardHeaderType != null
    dto.oddsCardHeaderType.outcomesTemplateType1 == entity.outcomesTemplateType1
    dto.oddsCardHeaderType.outcomesTemplateType2 == entity.outcomesTemplateType2
    dto.oddsCardHeaderType.outcomesTemplateType3 == entity.outcomesTemplateType3
    dto.disabled == entity.disabled
    dto.showInPlay == entity.showInPlay
    dto.isOutrightSport == entity.isOutrightSport
    dto.isMultiTemplateSport == entity.isMultiTemplateSport
    dto.tabs != null
    dto.tabs.tabLive != null
    dto.tabs.tabLive.tablabel == entity.tabLive.tablabel
    dto.tabs.tabLive.visible == entity.tabLive.visible
    dto.tabs.tabMatches != null
    dto.tabs.tabMatches.tablabel == entity.tabMatches.tablabel
    dto.tabs.tabMatches.visible == entity.tabMatches.visible
    dto.tabs.tabOutrights != null
    dto.tabs.tabOutrights.tablabel == entity.tabOutrights.tablabel
    dto.tabs.tabOutrights.visible == entity.tabOutrights.visible
    dto.tabs.tabSpecials != null
    dto.tabs.tabSpecials.tablabel == entity.tabSpecials.tablabel
    dto.tabs.tabSpecials.visible == entity.tabSpecials.visible
    dto.defaultTab == entity.defaultTab
    dto.inApp == entity.inApp.toString()
  }

  def "find by brand excludes 'public' form uri if it appears at the beginning of the string"() {
    given:
    def brand = 'rcomb'
    def disabled = false


    def entity = new Sport()
    entity.uriLarge = 'public/large-public'
    entity.uriMedium = 'public/medium-public'
    entity.uriSmall = 'public/small-public'
    entity.uriLargeIcon = 'public/large-public-icon'
    entity.uriMediumIcon = 'public/medium-public-icon'
    entity.uriSmallIcon = 'public/small-public-icon'

    repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand,disabled) >> [entity]

    when:
    def list = service.find(brand)

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

  def "find by brand"() {
    given:
    def brand = 'ladbrokes'
    def disabled = false

    def filename = new Filename()
    filename.filename = 'file.txt'

    def tabLive = new Tab()
    tabLive.tablabel = 'Live'
    tabLive.visible = true

    def tabMatches = new Tab()
    tabMatches.tablabel = 'Games'
    tabMatches.visible = true

    def tabOutrights = new Tab()
    tabOutrights.tablabel = 'Outrights'
    tabOutrights.visible = true

    def tabSpecials = new Tab()
    tabSpecials.tablabel = 'Specials'
    tabSpecials.visible = true

    def entity = new Sport()
    entity.id = 'ID'
    entity.filename = filename
    entity.uriLarge = '/uri-large'
    entity.uriMedium = '/uri-medium'
    entity.uriSmall = '/uri-small'
    entity.widthLarge = 32
    entity.widthMedium = 24
    entity.widthSmall = 16
    entity.heightLarge = 30
    entity.heightMedium = 20
    entity.heightSmall = 10
    entity.uriLargeIcon = 'uri-large-icon'
    entity.uriMediumIcon = 'uri-medium-icon'
    entity.uriSmallIcon = 'uri-small-icon'
    entity.svg = '<svg/>'
    entity.svgId = '#icon-esports'
    entity.alt = 'esports'
    entity.imageTitle = 'ESports'
    entity.categoryId = 99
    entity.typeIds = '111,222,333'
    entity.ssCategoryCode = 'ESPORTS'
    entity.targetUri = '/esports'
    entity.dispSortName = 'MR'
    entity.primaryMarkets = '|Match Betting|'
    entity.viewByFilters = 'filter1, filter2'
    entity.outcomesTemplateType1 = 'homeDrawAwayTypeA'
    entity.outcomesTemplateType2 = 'homeDrawAwayTypeB'
    entity.outcomesTemplateType3 = 'homeDrawAwayTypeC'
    entity.disabled = true
    entity.showInPlay = true
    entity.isOutrightSport = true
    entity.isMultiTemplateSport = true
    entity.tabLive = tabLive
    entity.tabMatches = tabMatches
    entity.tabOutrights = tabOutrights
    entity.tabSpecials = tabSpecials
    entity.defaultTab = 'specials'
    entity.inApp = true

    repository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand,disabled) >> [entity]

    when:
    def list = service.find(brand)

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
    dto.svg == entity.svg
    dto.svgId == entity.svgId
    dto.alt == entity.alt
    dto.imageTitle == entity.imageTitle
    dto.categoryId == entity.categoryId.toString()
    dto.typeIds.size() == 3
    dto.typeIds == ['111', '222', '333']
    dto.ssCategoryCode == entity.ssCategoryCode
    dto.targetUri == entity.targetUri
    dto.dispSortName.size() == 1
    dto.dispSortName == ['MR']
    dto.primaryMarkets == entity.primaryMarkets
    dto.viewByFilters.size() == 2
    dto.viewByFilters == VIEW_BY_FILTERS
    dto.oddsCardHeaderType != null
    dto.oddsCardHeaderType.outcomesTemplateType1 == entity.outcomesTemplateType1
    dto.oddsCardHeaderType.outcomesTemplateType2 == entity.outcomesTemplateType2
    dto.oddsCardHeaderType.outcomesTemplateType3 == entity.outcomesTemplateType3
    dto.disabled == entity.disabled
    dto.showInPlay == entity.showInPlay
    dto.isOutrightSport == entity.isOutrightSport
    dto.isMultiTemplateSport == entity.isMultiTemplateSport
    dto.tabs != null
    dto.tabs.tabLive != null
    dto.tabs.tabLive.tablabel == entity.tabLive.tablabel
    dto.tabs.tabLive.visible == entity.tabLive.visible
    dto.tabs.tabMatches != null
    dto.tabs.tabMatches.tablabel == entity.tabMatches.tablabel
    dto.tabs.tabMatches.visible == entity.tabMatches.visible
    dto.tabs.tabOutrights != null
    dto.tabs.tabOutrights.tablabel == entity.tabOutrights.tablabel
    dto.tabs.tabOutrights.visible == entity.tabOutrights.visible
    dto.tabs.tabSpecials != null
    dto.tabs.tabSpecials.tablabel == entity.tabSpecials.tablabel
    dto.tabs.tabSpecials.visible == entity.tabSpecials.visible
    dto.defaultTab == entity.defaultTab
    dto.inApp == entity.inApp.toString()
  }
}
