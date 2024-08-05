package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CouponStatsWidget;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CouponStatsWidgetService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CouponStatsWidgetPublicApi implements Public {

  private final CouponStatsWidgetService couponStatsWidgetService;

  public CouponStatsWidgetPublicApi(CouponStatsWidgetService couponStatsWidgetService) {
    this.couponStatsWidgetService = couponStatsWidgetService;
  }

  @GetMapping("/coupon-stats-widget/brand/{brand}")
  public CouponStatsWidget findByBrand(@PathVariable String brand) {

    return couponStatsWidgetService.readByBrand(brand).orElseThrow(NotFoundException::new);
  }
}
