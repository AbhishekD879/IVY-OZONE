package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.CouponMarketSelectorDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.CouponMarketSelectorPublicService;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class CouponMarketSelectorApi implements Public {
  private final CouponMarketSelectorPublicService couponMarketSelectorPublicService;

  @GetMapping("{brand}/coupon-market-selector")
  public List<CouponMarketSelectorDto> findByBrand(@PathVariable("brand") String brand) {
    return couponMarketSelectorPublicService.findByBrand(brand);
  }
}
