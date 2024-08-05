package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.CouponSegmentDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.CouponSegmentPublicService;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class CouponSegmentApi implements Public {
  private final CouponSegmentPublicService couponSegmentPublicService;

  @GetMapping("{brand}/coupon-segments")
  public List<CouponSegmentDto> findByBrand(@PathVariable("brand") String brand) {
    return couponSegmentPublicService.findByBrand(brand);
  }
}
