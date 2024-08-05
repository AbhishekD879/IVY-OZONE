package com.ladbrokescoral.oxygen.cms.api.service.sporttab.checker;

import com.egalacoral.spark.siteserver.model.Coupon;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabNames;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class CouponsTabEventsChecker extends EventsChecker {

  private final SiteServeService siteServeService;
  private final String brand;

  public CouponsTabEventsChecker(
      ScheduledTaskExecutor scheduledTaskExecutor,
      SiteServeService siteServeService,
      SportTabService sportTabService,
      TierCategoriesCache tierCategoriesCache,
      String brand) {
    super(scheduledTaskExecutor, sportTabService, tierCategoriesCache);
    this.siteServeService = siteServeService;
    this.brand = brand;
  }

  @Override
  protected void doCheck() {
    Map<Integer, List<Coupon>> couponsGroupedByCategoryId =
        siteServeService.getCouponsForTodaysAndUpcomingIn24hEvents(brand).stream()
            .collect(Collectors.groupingBy(coupon -> Integer.valueOf(coupon.getCategoryId())));

    List<SportTab> allCouponsTabs =
        sportTabService.findAllEnabledTabsByName(brand, SportTabNames.COUPONS);

    log.info("[{}] Found coupons for sports [{}]", brand, couponsGroupedByCategoryId.keySet());

    for (SportTab tab : allCouponsTabs) {
      Integer categoryId = tab.getSportId();
      List<Coupon> sportCoupons =
          couponsGroupedByCategoryId.getOrDefault(categoryId, Collections.emptyList());

      boolean hasCoupons = !sportCoupons.isEmpty();

      log.debug(
          "[{}] Try update couponTab [id={} sport={}] with hasEvents={}",
          brand,
          tab.getId(),
          categoryId,
          hasCoupons);
      sportTabService.updateHasEvents(brand, categoryId, SportTabNames.COUPONS, hasCoupons);
    }
  }
}
