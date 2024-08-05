package com.ladbrokescoral.oxygen.cms.api.service

import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier
import com.ladbrokescoral.oxygen.cms.api.repository.PopularTabRepository
import com.ladbrokescoral.oxygen.cms.api.repository.SportTabRepository
import com.ladbrokescoral.oxygen.cms.api.repository.TrendingTabRepository
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.Tier1SportTabsTemplate
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.Tier2SportTabsTemplate
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.UntiedSportTabsTemplate
import spock.lang.Specification

class SportTabInitServiceSpec extends Specification {

  SportTabRepository sportTabRepositoryMock
  TrendingTabRepository trendingTabRepository;
  PopularTabRepository popularTabRepository;
  SportTabService sportTabService
  UntiedSportTabsTemplate untiedSportTabsTemplate


  def setup() {
    sportTabRepositoryMock = Mock(SportTabRepository.class)
    trendingTabRepository = Mock(TrendingTabRepository.class)
    popularTabRepository = Mock(PopularTabRepository.class)
    untiedSportTabsTemplate = new UntiedSportTabsTemplate()

    sportTabService = new SportTabService(sportTabRepositoryMock,
        Arrays.asList(new Tier1SportTabsTemplate(),
        new Tier2SportTabsTemplate(),
        new UntiedSportTabsTemplate()), trendingTabRepository, popularTabRepository)
  }

  def "tabs from tier1 should be saved for football with special configuration"() {
    given: "SportCategory football"
    SportCategory sport = new SportCategory()
    sport.setBrand("bma")
    sport.setCategoryId(16)
    sport.setSsCategoryCode("FOOTBALL")
    sport.setTier(SportTier.TIER_1)

    when:
    sportTabService.createTabs(sport)

    then: "save 6 sportTabs from tier1 for football"
    1 * sportTabRepositoryMock.saveAll(Arrays.asList(
        SportTab.builder().name("matches").displayName("Matches")
        .sortOrder(1.0).enabled(true).brand("bma").sportId(16).build(),
        SportTab.builder().name("live").displayName("In-Play")
        .sortOrder(2.0).enabled(true).brand("bma").sportId(16).build(),
        SportTab.builder().name("competitions").displayName("Competitions")
        .sortOrder(3.0).enabled(true).brand("bma").sportId(16).build(),
        SportTab.builder().name("coupons").displayName("Coupons")
        .sortOrder(4.0).enabled(true)
        .checkEvents(true).brand("bma").sportId(16).build(),
        SportTab.builder().name("outrights").displayName("Outrights")
        .sortOrder(5.0).enabled(true).brand("bma").sportId(16).build(),
        SportTab.builder().name("specials").displayName("Specials")
        .sortOrder(7.0).enabled(true).checkEvents(true)
        .brand("bma").sportId(16).build(),
        SportTab.builder().name("jackpot").displayName("Jackpot")
        .sortOrder(6.0).enabled(true).checkEvents(true)
        .brand("bma").sportId(16).build(),
        SportTab.builder().name("popularbets").displayName("Popular Bets")
        .sortOrder(8.0).enabled(true).checkEvents(false)
        .brand("bma").sportId(16).build()
        ))
  }

  def "tabs from tier1 should be saved for basketball"() {
    given: "SportCategory basketball"
    SportCategory sport = new SportCategory()
    sport.setBrand("bma")
    sport.setCategoryId(6)
    sport.setSsCategoryCode("BASKETBALL")
    sport.setTier(SportTier.TIER_1)

    when:
    sportTabService.createTabs(sport)

    then: "save 4 sportTabs from tier1 for basketball"
    1 * sportTabRepositoryMock.saveAll(Arrays.asList(
        SportTab.builder().name("matches").displayName("Matches")
        .sortOrder(1.0).enabled(true).brand("bma").sportId(6).build(),
        SportTab.builder().name("live").displayName("In-Play")
        .sortOrder(2.0).enabled(true).brand("bma").sportId(6).build(),
        SportTab.builder().name("competitions").displayName("Competitions")
        .sortOrder(3.0).enabled(true).brand("bma").sportId(6).build(),
        SportTab.builder().name("coupons").displayName("Coupons")
        .sortOrder(4.0).enabled(true).checkEvents(true)
        .brand("bma").sportId(6).build(),
        SportTab.builder().name("outrights").displayName("Outrights")
        .sortOrder(5.0).enabled(true).brand("bma").sportId(6).build(),
        SportTab.builder().name("specials").displayName("Specials")
        .sortOrder(7.0).enabled(true).checkEvents(true)
        .brand("bma").sportId(6).build()
        ))
  }

  def "tabs from tier2 should be saved for snooker"() {
    given: "SportCategory snooker"
    SportCategory sport = new SportCategory()
    sport.setBrand("bma")
    sport.setCategoryId(32)
    sport.setSsCategoryCode("SNOOKER")
    sport.setTier(SportTier.TIER_2)

    when:
    sportTabService.createTabs(sport)

    then: "save 4 sportTabs from tier2 for snooker"
    1 * sportTabRepositoryMock.saveAll(Arrays.asList(
        SportTab.builder().name("matches").displayName("Matches")
        .sortOrder(1.0).enabled(true).checkEvents(true)
        .brand("bma").sportId(32).build(),
        SportTab.builder().name("competitions").displayName("Competitions")
        .sortOrder(2.0).enabled(true).checkEvents(true)
        .brand("bma").sportId(32).build(),
        SportTab.builder().name("outrights").displayName("Outrights")
        .sortOrder(3.0).enabled(true).checkEvents(true)
        .brand("bma").sportId(32).build(),
        SportTab.builder().name("coupons").displayName("Coupons")
        .sortOrder(4.0).enabled(false)
        .brand("bma").sportId(32).build(),
        SportTab.builder().name("specials").displayName("Specials")
        .sortOrder(5.0).enabled(true).checkEvents(true)
        .brand("bma").sportId(32).build()
        ))
  }

  def "tabs from tier2 should be saved for boxing"() {
    given: "SportCategory boxing"
    SportCategory sport = new SportCategory()
    sport.setBrand("bma")
    sport.setCategoryId(9)
    sport.setSsCategoryCode("BOXING")
    sport.setTier(SportTier.TIER_2)

    when:
    sportTabService.createTabs(sport)

    then: "save 4 sportTabs from tier2 for boxing"
    1 * sportTabRepositoryMock.saveAll(Arrays.asList(
        SportTab.builder().name("matches").displayName("Fights")
        .sortOrder(1.0).enabled(true).checkEvents(true)
        .brand("bma").sportId(9).build(),
        SportTab.builder().name("competitions").displayName("Competitions")
        .sortOrder(2.0).enabled(true).checkEvents(true)
        .brand("bma").sportId(9).build(),
        SportTab.builder().name("outrights").displayName("Outrights")
        .sortOrder(3.0).enabled(true).checkEvents(true)
        .brand("bma").sportId(9).build(),
        SportTab.builder().name("coupons").displayName("Coupons")
        .sortOrder(4.0).enabled(false)
        .brand("bma").sportId(9).build(),
        SportTab.builder().name("specials").displayName("Specials")
        .sortOrder(5.0).enabled(true).checkEvents(true)
        .brand("bma").sportId(9).build()
        ))
  }

  def "tabs should not be saved for Greyhounds sport because it does not belong to any template"() {
    given: "SportCategory greyhounds"
    SportCategory sport = new SportCategory()
    sport.setBrand("bma")
    sport.setCategoryId(19)
    sport.setSsCategoryCode("GREYHOUNDS")
    sport.setTier(SportTier.UNTIED)

    when:
    sportTabService.createTabs(sport)

    then: "do not save any tabs for not configured greyhounds"
    0 * sportTabRepositoryMock.save(_ as List<SportTab>)
  }

  def "tabs should be saved for basketball if basketball sportCategory is created"() {
    given: "SportCategory basketball"
    SportCategory sport = new SportCategory()
    sport.setBrand("bma")
    sport.setCategoryId(6)
    sport.setSsCategoryCode("BASKETBALL")
    sport.setTier(SportTier.TIER_1)

    when:
    sportTabService.createTabs(sport)

    then: "save tabs for basketball"
    1 * sportTabRepositoryMock.saveAll(_ as List)
  }
  def "testIsValidForUntiedSportIfCondition" () {
    given: "SportCategory GREYHOUNDS"
    SportCategory sport = new SportCategory()
    sport.setBrand("bma")
    sport.setCategoryId(19)
    sport.setSsCategoryCode("GREYHOUNDS")
    sport.setTier(SportTier.UNTIED)
    when:
    boolean result = untiedSportTabsTemplate.isValidForSport(sport)
    then: "save tabs for Greyhounds"
    result
  }
  def "testIsValidForUntiedSportElseCondition" () {
    SportCategory sport = new SportCategory()
    sport.setBrand("bma")
    sport.setCategoryId(19)
    sport.setSsCategoryCode("GREYHOUNDS")
    sport.setTier(SportTier.TIER_1)
    when:
    boolean result = untiedSportTabsTemplate.isValidForSport(sport)
    then: "save tabs for Greyhounds"
    !result
  }
  def "getTabsBySportForUntiedHorseRacing"() {
    given: "SportCategory HorseRacing"
    SportCategory sport = new SportCategory()
    sport.setBrand("bma")
    sport.setCategoryId(21)
    sport.setSsCategoryCode("HORSERACING")
    sport.setTier(SportTier.UNTIED)
    when:
    sportTabService.createTabs(sport)
    then:
    1 * sportTabRepositoryMock.saveAll(_ as List)
  }
  def "tabs should not be saved for HorseRacing sport because it does not belong to any template"() {
    given: "SportCategory HorseRacing"
    SportCategory sport = new SportCategory()
    sport.setBrand("bma")
    sport.setCategoryId(21)
    sport.setSsCategoryCode("Random")


    when:
    untiedSportTabsTemplate.getTabsBySport(sport.getSsCategoryCode())
    then: "do not save any tabs for not configured greyhounds"
    0 * sportTabRepositoryMock.save(_ as List<SportTab>)
  }
}
