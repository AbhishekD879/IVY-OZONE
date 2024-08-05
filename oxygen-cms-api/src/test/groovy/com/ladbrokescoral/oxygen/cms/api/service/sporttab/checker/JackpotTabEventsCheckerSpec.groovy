package com.ladbrokescoral.oxygen.cms.api.service.sporttab.checker


import com.ladbrokescoral.oxygen.cms.api.entity.SportTab
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService
import spock.lang.Specification

class JackpotTabEventsCheckerSpec extends Specification {
  private SportTabService sportTabService
  private SiteServeService siteServeService
  private ScheduledTaskExecutor scheduledTaskExecutorMock
  private JackpotTabEventsChecker checker

  void setup() {
    sportTabService = Mock(SportTabService)
    siteServeService = Mock(SiteServeService)
    TierCategoriesCache tierCategoriesCache = Mock(TierCategoriesCache)
    scheduledTaskExecutorMock = Mock(ScheduledTaskExecutor)
    checker = new JackpotTabEventsChecker(scheduledTaskExecutorMock, siteServeService, sportTabService, tierCategoriesCache)

    scheduledTaskExecutorMock.execute(_ as Runnable) >> { args ->
      args[0].run()
    }
  }

  def "test jackpot tab was saved when hasEvents value has been changed"() {
    given: "one jackpot tab in storage"
    SportTab jackpotTab = SportTab.builder().name("jackpot")
        .brand("bma").hasEvents(false).build()
    sportTabService.findWithEnabledCheckEvents("jackpot") >> Collections.singletonList(jackpotTab)

    and: "Site serve has jackpot events"
    siteServeService.hasSiteServeJackpotEvents("bma") >> true

    when:
    checker.checkForEvents()

    then: "the same tab with changed hasEvents value is saved"
    1 * sportTabService.save(SportTab.builder()
        .name("jackpot").brand("bma").hasEvents(true).build())
  }

  def "test jackpot tab was not saved when hasEvents value has not been changed"() {
    given: "one jackpot tab in storage"
    sportTabService.findWithEnabledCheckEvents("jackpot") >> Collections.singletonList(SportTab.builder()
        .name("jackpot").brand("bma").hasEvents(false).build())

    and: "Site serve has jackpot events"
    siteServeService.hasSiteServeJackpotEvents("bma") >> false

    when:
    checker.checkForEvents()

    then: "hasEvents value is not changed and tab is not saved"
    0 * sportTabService.save(_ as SportTab)
  }
}
