package com.ladbrokescoral.oxygen.cms.api.service.sporttab.checker

import com.egalacoral.spark.siteserver.model.Coupon
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabNames
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService

import spock.lang.Specification

class CouponsTabEventsCheckerSpec extends Specification {
  private SportTabService sportTabService
  private SiteServeService siteServeService
  private EventsChecker couponsChecker
  private ScheduledTaskExecutor scheduledTaskExecutorMock

  void setup() {
    sportTabService = Mock(SportTabService)
    siteServeService = Mock(SiteServeService)
    TierCategoriesCache tierCategoriesCache = Mock(TierCategoriesCache)
    scheduledTaskExecutorMock = Mock(ScheduledTaskExecutor)
    couponsChecker = new CouponsTabEventsChecker(scheduledTaskExecutorMock, siteServeService, sportTabService, tierCategoriesCache, "bma")

    scheduledTaskExecutorMock.execute(_ as Runnable) >> { args ->
      args[0].run()
    }
  }


  def "Existing coupons tab are updated with hasEvents=true if at least one coupons found"() {
    given:
    siteServeService.getCouponsForTodaysAndUpcomingIn24hEvents("bma") >> [
      coupon(1, 16),
      coupon(2, 20)
    ]

    sportTabService.findAllEnabledTabsByName("bma", SportTabNames.COUPONS) >> [
      sportTab(16),
      sportTab(30)
    ]
    when:
    couponsChecker.checkForEvents()
    then:
    1 * sportTabService.updateHasEvents("bma", 16, SportTabNames.COUPONS, true)
    1 * sportTabService.updateHasEvents("bma", 30, SportTabNames.COUPONS, false)
    0 * sportTabService.updateHasEvents("bma", 20, SportTabNames.COUPONS, _ as boolean)
  }

  def "When no coupons at all, every tab updated with hasEvent=false"() {
    given:
    siteServeService.getCouponsForTodaysAndUpcomingIn24hEvents("bma") >> []

    sportTabService.findAllEnabledTabsByName("bma", SportTabNames.COUPONS) >> [
      sportTab(16),
      sportTab(30)
    ]
    when:
    couponsChecker.checkForEvents()
    then:
    1 * sportTabService.updateHasEvents("bma", 16, SportTabNames.COUPONS, false)
    1 * sportTabService.updateHasEvents("bma", 30, SportTabNames.COUPONS, false)
  }

  private Coupon coupon(int couponId, int categoryId) {
    def coupon = new Coupon()
    coupon.id = couponId
    coupon.categoryId = categoryId
    coupon
  }

  private SportTab sportTab(int categoryId) {
    return SportTab.builder()
        .brand("bma")
        .name("coupons")
        .enabled(true)
        .sportId(categoryId)
        .build()
  }
}
