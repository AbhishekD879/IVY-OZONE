package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CouponAndMarketSwitcher;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CouponAndMarketSwitcherWidgetService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CouponAndMarketSwitcherWidgetApi implements Public {

  public final CouponAndMarketSwitcherWidgetService couponAndMarketSwitcherWidgetService;

  public CouponAndMarketSwitcherWidgetApi(
      CouponAndMarketSwitcherWidgetService couponAndMarketSwitcherWidgetService) {
    this.couponAndMarketSwitcherWidgetService = couponAndMarketSwitcherWidgetService;
  }

  @GetMapping("/couponAndMarketSwitcherWidget/brand/{brand}")
  public CouponAndMarketSwitcher findByBrand(@PathVariable String brand) {
    return couponAndMarketSwitcherWidgetService
        .readByBrand(brand)
        .orElseThrow(NotFoundException::new);
  }
}
