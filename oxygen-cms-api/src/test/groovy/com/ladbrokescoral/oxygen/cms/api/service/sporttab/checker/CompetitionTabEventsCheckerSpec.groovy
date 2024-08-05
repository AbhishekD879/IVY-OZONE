package com.ladbrokescoral.oxygen.cms.api.service.sporttab.checker

import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabNames
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService
import com.ladbrokescoral.oxygen.cms.util.TierCategoriesHelper
import spock.lang.Specification

import static com.ladbrokescoral.oxygen.cms.util.CollectionUtilX.listOf
import static com.ladbrokescoral.oxygen.cms.util.CollectionUtilX.setOf

class CompetitionTabEventsCheckerSpec extends Specification {
  private static final int TIER2_CRICKET_SPORT_ID = 10
  private static final int TIER2_FOOTBALL_SPORT_ID = 16
  private static final SportTabNames COMPETITIONS_TAB_NAME = SportTabNames.COMPETITIONS
  private static final String CORAL_BRAND = "bma"
  private SportTabService sportTabService
  private TierCategoriesHelper tierCategoriesHelper
  private SiteServeService siteServeService
  private ScheduledTaskExecutor scheduledTaskExecutorMock
  private CompetitionsEventsChecker competitionsTabChecker

  void setup() {
    sportTabService = Mock(SportTabService)
    siteServeService = Mock(SiteServeService)
    TierCategoriesCache tierCategoriesCache = Mock(TierCategoriesCache)
    scheduledTaskExecutorMock = Mock(ScheduledTaskExecutor)

    tierCategoriesHelper = new TierCategoriesHelper()
    tierCategoriesCache.getCategories(CORAL_BRAND, SportTier.TIER_1) >> tierCategoriesHelper.getCategories(CORAL_BRAND, SportTier.TIER_1)
    tierCategoriesCache.getCategories(CORAL_BRAND, SportTier.TIER_2) >> tierCategoriesHelper.getCategories(CORAL_BRAND, SportTier.TIER_2)

    competitionsTabChecker = new CompetitionsEventsChecker(scheduledTaskExecutorMock, siteServeService, sportTabService, tierCategoriesCache, CORAL_BRAND)

    scheduledTaskExecutorMock.execute(_ as Runnable) >> { args ->
      args[0].run()
    }
  }

  def "should set hasEvents=true if there are new competition events"() {
    given: "hidden Competitions tab in storage"
    SportTab competitionsTabWithoutEvents = competitionsTab(TIER2_CRICKET_SPORT_ID, false)
    sportTabService.findAllForCheckingEvents(CORAL_BRAND, COMPETITIONS_TAB_NAME) >> listOf(competitionsTabWithoutEvents)

    def categories = mockSportsExisting(TIER2_CRICKET_SPORT_ID)

    and: "Site serve has Competitions events for Cricket"
    siteServeService.filterByCompetitionEvents(CORAL_BRAND, categories) >> setOf(TIER2_CRICKET_SPORT_ID)

    when:
    competitionsTabChecker.checkForEvents()

    then: "Cricket: Competitions tab set hasEvents=true"
    1 * sportTabService.save(competitionsTab(TIER2_CRICKET_SPORT_ID, true))
  }

  def "should set hasEvents=false if there are NO more competition events"() {
    given: "visible Competitions tab in storage"
    SportTab competitionsTabWithEvents = competitionsTab(TIER2_CRICKET_SPORT_ID, true)
    sportTabService.findAllForCheckingEvents(CORAL_BRAND, COMPETITIONS_TAB_NAME) >> listOf(competitionsTabWithEvents)

    def categories = mockSportsExisting(TIER2_CRICKET_SPORT_ID)

    and: "Site serve does NOT have Competitions events for Cricket"
    siteServeService.filterByCompetitionEvents(CORAL_BRAND, categories) >> setOf()

    when:
    competitionsTabChecker.checkForEvents()

    then: "Cricket: Competitions tab set hasEvents=false"
    1 * sportTabService.save(competitionsTab(TIER2_CRICKET_SPORT_ID, false))
  }

  def "should NOT change hasEvents value if there was and there are competition events still"() {
    given: "visible Competitions tab in storage"
    SportTab competitionsTabWithEvents = competitionsTab(TIER2_CRICKET_SPORT_ID, true)
    sportTabService.findAllForCheckingEvents(CORAL_BRAND, COMPETITIONS_TAB_NAME) >> listOf(competitionsTabWithEvents)

    def categories = mockSportsExisting(TIER2_CRICKET_SPORT_ID)

    and: "Site serve has Competitions events for Cricket"
    siteServeService.filterByCompetitionEvents(CORAL_BRAND, categories) >> setOf(TIER2_CRICKET_SPORT_ID)

    when:
    competitionsTabChecker.checkForEvents()

    then: "Cricket: Competitions tab does NOT changed hasEvents value"
    0 * sportTabService.save(competitionsTab(TIER2_CRICKET_SPORT_ID, true))
    0 * sportTabService.save(competitionsTab(TIER2_CRICKET_SPORT_ID, false))
  }

  def "should NOT change hasEvents value if there was NOT and there are NO competition events still"() {
    given: "hidden Competitions tab in storage"
    SportTab competitionsTabWithoutEvents = competitionsTab(TIER2_CRICKET_SPORT_ID, false)
    sportTabService.findAllForCheckingEvents(CORAL_BRAND, COMPETITIONS_TAB_NAME) >> listOf(competitionsTabWithoutEvents)

    def categories = mockSportsExisting(TIER2_CRICKET_SPORT_ID)

    and: "Site serve does NOT have Competitions events for Cricket"
    siteServeService.filterByCompetitionEvents(CORAL_BRAND, categories) >> setOf()

    when:
    competitionsTabChecker.checkForEvents()

    then: "Cricket: Competitions tab does NOT changed hasEvents value"
    0 * sportTabService.save(competitionsTab(TIER2_CRICKET_SPORT_ID, true))
    0 * sportTabService.save(competitionsTab(TIER2_CRICKET_SPORT_ID, false))
  }

  def "should check for Competitions only for Tier2 sports"() {
    given: "two Competitions tabs in storage"
    SportTab cricketTab = competitionsTab(TIER2_CRICKET_SPORT_ID, false)
    SportTab footballTab = competitionsTab(TIER2_FOOTBALL_SPORT_ID, false)
    sportTabService.findAllForCheckingEvents(CORAL_BRAND, COMPETITIONS_TAB_NAME) >> listOf(cricketTab, footballTab)
    def categories = mockSportsExisting(TIER2_CRICKET_SPORT_ID)

    when:
    competitionsTabChecker.checkForEvents()

    then: "Check events only for Tier2 sports"
    siteServeService.filterByCompetitionEvents(CORAL_BRAND, categories) >> setOf(TIER2_CRICKET_SPORT_ID)
  }

  def mockFindWithEnabledCheckEvents(SportTab matchesTab) {
    sportTabService.findAllForCheckingEvents(CORAL_BRAND, COMPETITIONS_TAB_NAME) >> Collections.singletonList(matchesTab)
  }

  SportTab competitionsTab() {
    return competitionsTab(TIER2_CRICKET_SPORT_ID, false)
  }

  SportTab competitionsTab(Integer sportId, boolean hasEvents) {
    return SportTab.builder()
        .name(SportTabNames.COMPETITIONS.nameLowerCase())
        .brand(CORAL_BRAND)
        .sportId(sportId)
        .checkEvents(true)
        .hasEvents(hasEvents)
        .build()
  }

  def "job should still working if Competitions tab checker throws an exception"() {
    given: "one Competitions tab in storage"
    sportTabService.findAllForCheckingEvents(CORAL_BRAND, COMPETITIONS_TAB_NAME) >> Collections.singletonList(competitionsTab(TIER2_CRICKET_SPORT_ID, false))
    mockSportsExisting(TIER2_CRICKET_SPORT_ID)

    and: "Site serve client thrown exception"
    siteServeService.filterByCompetitionEvents(_ as String, _ as List) >> { throw new Exception() }

    when:
    competitionsTabChecker.checkForEvents()

    then: "Job is handling exception"
    noExceptionThrown()
  }

  private List<SportCategory> mockSportsExisting(Integer... categoryIds) {
    def categories = new ArrayList()
    for (Integer categoryId : categoryIds) {
      def category = tierCategoriesHelper.find(CORAL_BRAND, categoryId)
      if (!category.isPresent()) {
        throw new IllegalArgumentException(categoryId + " isn't defined in TierCategoriesHelper")
      }
      categories.add(category.get())
    }
    return categories
  }

  private static SportCategory category(int categoryId) {
    SportCategory category = new SportCategory()
    category.setTier(SportTier.TIER_2)
    category.setCategoryId(categoryId)
  }
}
