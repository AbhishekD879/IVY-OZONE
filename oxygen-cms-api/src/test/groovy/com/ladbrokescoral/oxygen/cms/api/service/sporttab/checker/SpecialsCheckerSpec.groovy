package com.ladbrokescoral.oxygen.cms.api.service.sporttab.checker

import com.egalacoral.spark.siteserver.model.Event
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabNames
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService
import spock.lang.Specification

class SpecialsCheckerSpec extends Specification {
  public static final String CORAL_BRAND = "bma"
  private SportTabService sportTabService
  private SiteServeService siteServeService
  private EventsChecker eventsChecker
  private ScheduledTaskExecutor scheduledTaskExecutorMock
  private TierCategoriesCache tierCategoriesCache;

  void setup() {
    sportTabService = Mock(SportTabService)
    siteServeService = Mock(SiteServeService)
    scheduledTaskExecutorMock = Mock(ScheduledTaskExecutor)
    tierCategoriesCache = Mock(TierCategoriesCache)
    eventsChecker = new SpecialsChecker(scheduledTaskExecutorMock, siteServeService, sportTabService, tierCategoriesCache, CORAL_BRAND)

    scheduledTaskExecutorMock.execute(_ as Runnable) >> { args ->
      args[0].run()
    }
  }

  def "When no specials found then specials tab updated with hasEvents=false"() {
    given:
    siteServeService.getSportSpecials(CORAL_BRAND, 16) >> []
    tierCategoriesCache.getCategoryIds(CORAL_BRAND, SportTier.TIER_1) >> [16]
    tierCategoriesCache.getCategoryIds(CORAL_BRAND, SportTier.TIER_2) >> [5]
    when:
    eventsChecker.checkForEvents()
    then:
    1 * sportTabService.updateHasEvents(CORAL_BRAND, 16, SportTabNames.SPECIALS, false)
    0 * sportTabService.updateHasEvents(CORAL_BRAND, 20, SportTabNames.SPECIALS, _ as boolean)
  }

  def "When sport contains specials it's updated"() {
    given:
    tierCategoriesCache.getCategoryIds(CORAL_BRAND, SportTier.TIER_1) >> [16]
    tierCategoriesCache.getCategoryIds(CORAL_BRAND, SportTier.TIER_2) >> []
    siteServeService.getSportSpecials(CORAL_BRAND, 16) >> [event()]
    when:
    eventsChecker.checkForEvents()
    then:
    1 * sportTabService.updateHasEvents(CORAL_BRAND, 16, SportTabNames.SPECIALS, true)
  }

  private Event event() {
    def event = new Event()
    event.id = 123
    return event
  }
}
