package com.ladbrokescoral.oxygen.cms.api.service.sporttab.checker

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

class OutrightsTabEventsCheckerSpec extends Specification {
  private static final int TIER2_CRICKET_SPORT_ID = 10
  private static final int TIER2_FOOTBALL_SPORT_ID = 16
  private static final SportTabNames OUTRIGHTS_TAB_NAME = SportTabNames.OUTRIGHTS
  private static final String CORAL_BRAND = "bma"
  private SportTabService sportTabService
  private SiteServeService siteServeService
  private ScheduledTaskExecutor scheduledTaskExecutorMock
  private OutrightsTabEventsChecker outrightsTabChecker
  private TierCategoriesHelper tierCategoriesCacheMock

  void setup() {
    sportTabService = Mock(SportTabService)
    siteServeService = Mock(SiteServeService)
    TierCategoriesCache tierCategoriesCache = Mock(TierCategoriesCache)
    scheduledTaskExecutorMock = Mock(ScheduledTaskExecutor)

    tierCategoriesCacheMock = new TierCategoriesHelper()
    tierCategoriesCache.getCategoryIds(CORAL_BRAND, SportTier.TIER_1) >> tierCategoriesCacheMock.getCategoryIds(SportTier.TIER_1)
    tierCategoriesCache.getCategoryIds(CORAL_BRAND, SportTier.TIER_2) >> tierCategoriesCacheMock.getCategoryIds(SportTier.TIER_2)

    outrightsTabChecker = new OutrightsTabEventsChecker(scheduledTaskExecutorMock, siteServeService, sportTabService, tierCategoriesCache, CORAL_BRAND)

    scheduledTaskExecutorMock.execute(_ as Runnable) >> { args ->
      args[0].run()
    }
  }

  def "should set hasEvents=true if there are new outright events"() {
    given: "hidden Outright tab in storage"
    SportTab outrightTabWithoutEvents = outrightsTab(TIER2_CRICKET_SPORT_ID, false)
    sportTabService.findAllForCheckingEvents(CORAL_BRAND, OUTRIGHTS_TAB_NAME) >> listOf(outrightTabWithoutEvents)

    and: "Site serve has Outright events for Cricket"
    siteServeService.filterByOutrightEvents(CORAL_BRAND, setOf(TIER2_CRICKET_SPORT_ID)) >> setOf(TIER2_CRICKET_SPORT_ID)

    when:
    outrightsTabChecker.checkForEvents()

    then: "Cricket: Outright tab set hasEvents=true"
    1 * sportTabService.save(outrightsTab(TIER2_CRICKET_SPORT_ID, true))
  }

  def "should set hasEvents=false if there are NO more outright events"() {
    given: "visible Outright tab in storage"
    SportTab outrightTabWithEvents = outrightsTab(TIER2_CRICKET_SPORT_ID, true)
    sportTabService.findAllForCheckingEvents(CORAL_BRAND, OUTRIGHTS_TAB_NAME) >> listOf(outrightTabWithEvents)

    and: "Site serve does NOT have Outright events for Cricket"
    siteServeService.filterByOutrightEvents(CORAL_BRAND, setOf(TIER2_CRICKET_SPORT_ID)) >> setOf()

    when:
    outrightsTabChecker.checkForEvents()

    then: "Cricket: Outright tab set hasEvents=false"
    1 * sportTabService.save(outrightsTab(TIER2_CRICKET_SPORT_ID, false))
  }

  def "should NOT change hasEvents value if there was and there are outright events still"() {
    given: "visible Outright tab in storage"
    SportTab outrightTabWithEvents = outrightsTab(TIER2_CRICKET_SPORT_ID, true)
    sportTabService.findAllForCheckingEvents(CORAL_BRAND, OUTRIGHTS_TAB_NAME) >> listOf(outrightTabWithEvents)

    and: "Site serve has Outright events for Cricket"
    siteServeService.filterByOutrightEvents(CORAL_BRAND, setOf(TIER2_CRICKET_SPORT_ID)) >> setOf(TIER2_CRICKET_SPORT_ID)

    when:
    outrightsTabChecker.checkForEvents()

    then: "Cricket: Outright tab does NOT changed hasEvents value"
    0 * sportTabService.save(outrightsTab(TIER2_CRICKET_SPORT_ID, false))
    0 * sportTabService.save(outrightsTab(TIER2_CRICKET_SPORT_ID, false))
  }

  def "should NOT change hasEvents value if there was NOT and there are NO outright events still"() {
    given: "hidden Outright tab in storage"
    SportTab outrightTabWithoutEvents = outrightsTab(TIER2_CRICKET_SPORT_ID, false)
    sportTabService.findAllForCheckingEvents(CORAL_BRAND, OUTRIGHTS_TAB_NAME) >> listOf(outrightTabWithoutEvents)

    and: "Site serve does NOT have Outright events for Cricket"
    siteServeService.filterByOutrightEvents(CORAL_BRAND, setOf(TIER2_CRICKET_SPORT_ID)) >> setOf()

    when:
    outrightsTabChecker.checkForEvents()

    then: "Cricket: Outright tab does NOT changed hasEvents value"
    0 * sportTabService.save(outrightsTab(TIER2_CRICKET_SPORT_ID, true))
    0 * sportTabService.save(outrightsTab(TIER2_CRICKET_SPORT_ID, false))
  }

  def "should check for Outrights only for Tier2 sports"() {
    given: "two Outrights tabs in storage"
    SportTab cricketTab = outrightsTab(TIER2_CRICKET_SPORT_ID, false)
    SportTab footballTab = outrightsTab(TIER2_FOOTBALL_SPORT_ID, false)
    sportTabService.findAllForCheckingEvents(CORAL_BRAND, OUTRIGHTS_TAB_NAME) >> listOf(cricketTab, footballTab)

    when:
    outrightsTabChecker.checkForEvents()

    then: "Check events only for Tier2 sports"
    siteServeService.filterByOutrightEvents(CORAL_BRAND, setOf(TIER2_CRICKET_SPORT_ID)) >> setOf(TIER2_CRICKET_SPORT_ID)
  }

  SportTab outrightsTab(Integer sportId, boolean hasEvents) {
    return SportTab.builder()
        .name(SportTabNames.OUTRIGHTS.nameLowerCase())
        .brand(CORAL_BRAND)
        .sportId(sportId)
        .checkEvents(true)
        .hasEvents(hasEvents)
        .build()
  }

  def "job should still working if Outrights tab checker throws an exception"() {
    given: "one Outrights tab in storage"
    sportTabService.findAllForCheckingEvents(CORAL_BRAND, OUTRIGHTS_TAB_NAME) >> Collections.singletonList(outrightsTab(TIER2_CRICKET_SPORT_ID, false))

    and: "Site serve client thrown exception"
    siteServeService.filterByOutrightEvents(_ as String, _ as Set) >> { throw new Exception() }

    when:
    outrightsTabChecker.checkForEvents()

    then: "Job is handling exception"
    noExceptionThrown()
  }
}
