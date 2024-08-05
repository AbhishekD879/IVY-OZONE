package com.ladbrokescoral.oxygen.cms.api.service.public_api

import com.ladbrokescoral.oxygen.cms.api.TestUtil
import com.ladbrokescoral.oxygen.cms.api.dto.SportTabConfigListDto
import com.ladbrokescoral.oxygen.cms.api.entity.OddsCardHeaderType
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository
import com.ladbrokescoral.oxygen.cms.api.repository.SportTabRepository
import com.ladbrokescoral.oxygen.cms.api.service.InplayStatsDisplayService
import com.ladbrokescoral.oxygen.cms.api.service.InplayStatsSortingService
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService
import spock.lang.Specification

class SportTabsPublicServiceSpecification extends Specification {
  private static final String CORAL_BRAND = "bma"

  SportCategoryRepository categoryRepository
  SportTabRepository tabRepository
  SportCategoryPublicService service
  SegmentService segmentService
  InplayStatsDisplayService statsDisplayService
  InplayStatsSortingService statsSortingService

  def setup() {
    categoryRepository = Mock(SportCategoryRepository)
    tabRepository = Mock(SportTabRepository)
    segmentService=Mock(SegmentService)
    statsDisplayService = Mock(InplayStatsDisplayService)
    statsSortingService = Mock(InplayStatsSortingService)
    service = new SportCategoryPublicService(categoryRepository, tabRepository,segmentService,statsDisplayService,statsSortingService)
  }

  def "should return valid sport configurations"() {
    given:
    def cricketSportId = 10
    def brand = CORAL_BRAND
    categoryRepository.findByBrandAndCategoryId(brand, cricketSportId) >> Collections.singletonList(cricketCategory())
    List<SportTab> cricketTabs = new TabsBuilder(brand, cricketSportId)
        .addTab("Matches")
        .addTab("Competitions")
        .addTab("Outrights")
        .addTab("Coupons", false, false, false)
        .build()

    tabRepository.findAllByBrandAndSportId(brand, cricketSportId) >> cricketTabs

    def expected = TestUtil.deserializeWithJackson("service/public_api/sport-tabs/10.json", SportTabConfigListDto.class)

    when:
    SportTabConfigListDto actual = service.getSportTabs(brand, cricketSportId)

    then:
    expected == actual
  }

  def "should return valid Outright sport configurations"() {
    given:
    def cyclingSportId = 12
    def brand = CORAL_BRAND

    def cycling = new SportCategory()
    cycling.setCategoryId(cyclingSportId)
    cycling.setTier(SportTier.TIER_2)
    cycling.setOutrightSport(true)
    cycling.setMultiTemplateSport(false)
    cycling.setImageTitle("Cycling")
    cycling.setTargetUri("sport/cycling")
    cycling.setDispSortNames("MR,HH,MH,WH") // should not convert
    cycling.setPrimaryMarkets("|Match Betting|,|Match Betting Head/Head|,|Handicap Match Result|") // should not convert
    cycling.setBrand(CORAL_BRAND)
    cycling.setOddsCardHeaderType(null)
    categoryRepository.findByBrandAndCategoryId(brand, cyclingSportId) >> Collections.singletonList(cycling)
    List<SportTab> cyclingTabs = new TabsBuilder(brand, cyclingSportId)
        .addTab("Events", "matches")
        .addTab("Competitions")
        .addTab("Outrights")
        .addTab("Coupons", false, false, false)
        .build()

    tabRepository.findAllByBrandAndSportId(brand, cyclingSportId) >> cyclingTabs

    def expected = TestUtil.deserializeWithJackson("service/public_api/sport-tabs/12.json", SportTabConfigListDto.class)

    when:
    SportTabConfigListDto actual = service.getSportTabs(brand, cyclingSportId)

    then:
    expected == actual
  }

  def "should return valid Football sport configurations"() {
    given:
    def footballSportId = 16
    def brand = CORAL_BRAND

    def football = new SportCategory()
    football.setCategoryId(footballSportId)
    football.setTier(SportTier.TIER_1)
    football.setOutrightSport(false)
    football.setImageTitle("Football")
    football.setSsCategoryCode("FOOTBALL")
    football.setMultiTemplateSport(false)
    football.setTargetUri("sport/football")
    football.setBrand(CORAL_BRAND)
    football.setOddsCardHeaderType(OddsCardHeaderType.HOME_DRAW_AWAY_TYPE)

    categoryRepository.findByBrandAndCategoryId(brand, footballSportId) >> Collections.singletonList(football)
    List<SportTab> footballTabs = new TabsBuilder(brand, footballSportId)
        .addTab("Matches")
        .addTab("In-Play", "live")
        .addTab("Competitions")
        .addTab("Coupons")
        .addTab("Outrights")
        .addTab("Jackpot")
        .addTab("Specials")
        .addTab("Popular Bets","popularbets")
        .build()

    tabRepository.findAllByBrandAndSportId(brand, footballSportId) >> footballTabs

    def expected = TestUtil.deserializeWithJackson("service/public_api/sport-tabs/16.json", SportTabConfigListDto.class)

    when:
    SportTabConfigListDto actual = service.getSportTabs(brand, footballSportId)

    then:
    expected == actual
  }


  def "should sport tabs sorted by sort order with hidden on top"() {
    given:
    def cricketSportId = 10
    def brand = CORAL_BRAND
    categoryRepository.findByBrandAndCategoryId(brand, cricketSportId) >> Collections.singletonList(cricketCategory())
    List<SportTab> cricketTabs = new TabsBuilder(brand, cricketSportId)
        .addTab("Matches")
        .addTab("Competitions", true, true, false)
        .addTab("Outrights", true, false, false)
        .addTab("Coupons", false, false, false)
        .build()
    tabRepository.findAllByBrandAndSportId(brand, cricketSportId) >> cricketTabs

    when:
    SportTabConfigListDto actualConfig = service.getSportTabs(brand, cricketSportId)

    then:
    // order: competitions, coupons, matches, outrights
    actualConfig.tabs.size() == 4
    actualConfig.tabs.get(0).name == "competitions"
    actualConfig.tabs.get(0).hidden

    actualConfig.tabs.get(1).name == "coupons"
    actualConfig.tabs.get(1).hidden

    actualConfig.tabs.get(2).name == "matches"
    ! actualConfig.tabs.get(2).hidden

    actualConfig.tabs.get(3).name == "outrights"
    ! actualConfig.tabs.get(3).hidden
  }

  SportCategory cricketCategory() {
    def category = new SportCategory()
    category.setCategoryId(10)
    category.setTier(SportTier.TIER_2)
    category.setOutrightSport(false)
    category.setMultiTemplateSport(true)
    category.setImageTitle("Cricket")
    category.setTargetUri("sport/cricket")
    category.setDispSortNames("MR,HH /MH,,  WH")
    category.setPrimaryMarkets("|Match Betting|,|Match Betting Head/Head|,|Handicap Match Result|")
    category.setBrand(CORAL_BRAND)
    category.setOddsCardHeaderType(OddsCardHeaderType.ONE_TWO_TYPE)
    return category
  }

  class TabsBuilder {
    private List<SportTab> tabs
    private int sortOrder
    String brand
    int sportId

    TabsBuilder(String brand, int sportId) {
      this.brand = brand
      this.sportId = sportId
      this.tabs = new ArrayList<>()
      this.sortOrder = 0
    }

    TabsBuilder addTab(String displayName) {
      this.addTab(displayName, true, true, true)
      return this
    }

    TabsBuilder addTab(String displayName, boolean enabled, boolean checkEvents, boolean hasEvents) {
      tabs.add(SportTab.builder()
          .brand(brand)
          .sportId(sportId)
          .enabled(enabled)
          .checkEvents(checkEvents)
          .hasEvents(hasEvents)
          .name(displayName.toLowerCase())
          .displayName(displayName)
          .sortOrder(++this.sortOrder)
          .build())
      return this
    }

    TabsBuilder addTab(String displayName, String name) {
      tabs.add(SportTab.builder()
          .brand(brand)
          .sportId(sportId)
          .enabled(true)
          .checkEvents(true)
          .hasEvents(true)
          .name(name)
          .displayName(displayName)
          .sortOrder(++this.sortOrder)
          .build())
      return this
    }

    List<SportTab> build() {
      return tabs
    }
  }
}
