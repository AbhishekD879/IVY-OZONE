package com.ladbrokescoral.oxygen.cms.api.service.sporttab.checker


import com.ladbrokescoral.oxygen.cms.api.entity.SportTab
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeServiceImpl
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabNames
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService
import com.ladbrokescoral.oxygen.cms.util.TierCategoriesHelper
import spock.lang.Specification

class MatchesTabEventsCheckerSpec extends Specification {
  private static final int TIER_2_SPORT_ID = 10
  private static final String CORAL_BRAND = "bma"
  private SportTabService sportTabService
  private TierCategoriesCache tierCategoriesCache
  private SiteServeService siteServeService
  private ScheduledTaskExecutor scheduledTaskExecutorMock
  private MatchesTabEventsChecker matchesTabChecker
  private TierCategoriesHelper tierCategoriesCacheMock

  void setup() {
    sportTabService = Mock(SportTabService)
    siteServeService = Mock(SiteServeServiceImpl)
    tierCategoriesCache = Mock(TierCategoriesCache)
    scheduledTaskExecutorMock = Mock(ScheduledTaskExecutor)
    matchesTabChecker = new MatchesTabEventsChecker(scheduledTaskExecutorMock, siteServeService, sportTabService, tierCategoriesCache, CORAL_BRAND)

    tierCategoriesCacheMock = new TierCategoriesHelper()
    tierCategoriesCache.getCategories(CORAL_BRAND, SportTier.TIER_1) >> tierCategoriesCacheMock.getCategories(CORAL_BRAND, SportTier.TIER_1)
    tierCategoriesCache.getCategories(CORAL_BRAND, SportTier.TIER_2) >> tierCategoriesCacheMock.getCategories(CORAL_BRAND, SportTier.TIER_2)

    scheduledTaskExecutorMock.execute(_ as Runnable) >> { args ->
      args[0].run()
    }
  }

  def "test set hasEvents=true for Matches tab if Live Or Upcoming events exists"() {
    given: "one matches tab in storage"
    def tab = this.matchesTab()
    mockFindWithEnabledCheckEvents(tab)
    def sportCategory = tierCategoriesCacheMock.find(CORAL_BRAND, tab.getSportId())

    and: "Site serve has Live AND Upcoming events"
    siteServeService.anyLiveOrUpcomingEventsExists(sportCategory.get()) >> true

    when:
    matchesTabChecker.checkForEvents()

    then: "the same tab with changed hasEvents value is saved"
    1 * sportTabService.save(matchesTab(true))
  }

  def "test set hasEvents=true for Golf Matches tab if Upcoming events exists"() {
    given: "one golf matches tab in storage"
    def tab = this.matchesTab(18,false)
    mockFindWithEnabledCheckEvents(tab)
    def sportCategory = tierCategoriesCacheMock.find(CORAL_BRAND, 18)

    siteServeService.anyLiveOrUpcomingEventsExists(sportCategory.get()) >> false
    ((SiteServeServiceImpl)siteServeService).anyLiveOrUpcomingEventsExistsForGolf(sportCategory.get()) >> true

    when:
    matchesTabChecker.checkForEvents()

    then: "the same tab with changed hasEvents value is saved"
    0 * sportTabService.save(matchesTab(true))
  }

  def "test set hasEvents=true for Golf Matches tab if Upcoming events doesn't exists"() {
    given: "one golf matches tab in storage"
    def tab = this.matchesTab(18,false)
    mockFindWithEnabledCheckEvents(tab)
    def sportCategory = tierCategoriesCacheMock.find(CORAL_BRAND, 18)

    siteServeService.anyLiveOrUpcomingEventsExists(sportCategory.get()) >> false
    ((SiteServeServiceImpl)siteServeService).anyLiveOrUpcomingEventsExistsForGolf(sportCategory.get()) >> false

    when:
    matchesTabChecker.checkForEvents()

    then: "the same tab with changed hasEvents value is saved"
    0 * sportTabService.save(matchesTab(true))
  }

  def mockFindWithEnabledCheckEvents(SportTab matchesTab) {
    sportTabService.findAllForCheckingEvents(CORAL_BRAND, SportTabNames.MATCHES) >> Collections.singletonList(matchesTab)
  }

  SportTab matchesTab() {
    return matchesTab(TIER_2_SPORT_ID, false)
  }

  SportTab matchesTab(boolean hasEvents) {
    return matchesTab(TIER_2_SPORT_ID, hasEvents)
  }

  SportTab matchesTab(Integer sportId, boolean hasEvents) {
    return SportTab.builder()
        .name("matches")
        .brand(CORAL_BRAND)
        .sportId(sportId)
        .checkEvents(true)
        .hasEvents(hasEvents)
        .build()
  }

  def "test Matches tab was NOT updated if Live Or Upcoming events do NOT exists"() {
    given: "one matches tab in storage"
    def matchesTab = this.matchesTab()
    mockFindWithEnabledCheckEvents(matchesTab)
    def sportCategory = tierCategoriesCacheMock.find(CORAL_BRAND, matchesTab.getSportId())

    and: "Site serve doesn't has matches events"
    siteServeService.anyLiveOrUpcomingEventsExists(sportCategory.get()) >> false

    when:
    matchesTabChecker.checkForEvents()

    then: "hasEvents value is NOT changed and tab is NOT saved"
    0 * sportTabService.save(_ as SportTab)
  }
}
