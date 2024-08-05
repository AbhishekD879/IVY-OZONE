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

class GolfMatchesTabEventsCheckerSpec extends Specification {
  private static final int TIER_2_SPORT_ID = 18
  private static final String CORAL_BRAND = "bma"
  private SportTabService sportTabService
  private TierCategoriesCache tierCategoriesCache
  private SiteServeService siteServeService
  private ScheduledTaskExecutor scheduledTaskExecutorMock
  private GolfMatchesTabEventsChecker checker
  private TierCategoriesHelper tierCategoriesCacheMock

  void setup() {
    sportTabService = Mock(SportTabService)
    siteServeService = Mock(SiteServeServiceImpl)
    tierCategoriesCache = Mock(TierCategoriesCache)
    scheduledTaskExecutorMock = Mock(ScheduledTaskExecutor)
    checker = new GolfMatchesTabEventsChecker(scheduledTaskExecutorMock, siteServeService, sportTabService, tierCategoriesCache, CORAL_BRAND)

    tierCategoriesCacheMock = new TierCategoriesHelper()
    // tierCategoriesCache.getCategories(CORAL_BRAND, SportTier.TIER_1) >> tierCategoriesCacheMock.getCategories(CORAL_BRAND, SportTier.TIER_1)
    tierCategoriesCache.getCategories(CORAL_BRAND, SportTier.TIER_2) >> tierCategoriesCacheMock.getCategories(CORAL_BRAND, SportTier.TIER_2)

    scheduledTaskExecutorMock.execute(_ as Runnable) >> { args ->
      args[0].run()
    }
  }
  def "test set hasEvents=true for Golf Matches tab if Live Or Upcoming events exists"() {
    given: "one golf matches tab in storage"
    def tab = this.matchesTab()
    mockFindWithEnabledCheckEvents(tab)
    def sportCategory = tierCategoriesCacheMock.find(CORAL_BRAND, tab.getSportId())

    and: "Site serve has Live AND Upcoming events"
    ((SiteServeServiceImpl)siteServeService).anyUpcomingEventsExistsForMatchesTabGolf(sportCategory.get()) >> true

    when:
    checker.checkForEvents()

    then: "the same tab with changed hasEvents value is saved"
    1 * sportTabService.save(matchesTab(true))
  }

  SportTab matchesTab() {
    return matchesTab(TIER_2_SPORT_ID, false)
  }

  SportTab matchesTab(boolean hasEvents) {
    return matchesTab(TIER_2_SPORT_ID, hasEvents)
  }
  SportTab matchesTab(Integer sportId, boolean hasEvents) {
    return SportTab.builder()
        .name("golf_matches")
        .displayName("Matches")
        .brand(CORAL_BRAND)
        .sportId(sportId)
        .checkEvents(true)
        .hasEvents(hasEvents)
        .build()
  }
  def mockFindWithEnabledCheckEvents(SportTab matchesTab) {
    sportTabService.findAllForCheckingEvents(CORAL_BRAND, SportTabNames.GOLF_MATCHES) >> Collections.singletonList(matchesTab)
  }
}
