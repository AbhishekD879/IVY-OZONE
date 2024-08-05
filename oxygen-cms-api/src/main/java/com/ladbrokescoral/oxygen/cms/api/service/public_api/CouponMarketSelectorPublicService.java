package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.CouponMarketSelectorDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.CouponMarketSelectorMapper;
import com.ladbrokescoral.oxygen.cms.api.service.ApiService;
import com.ladbrokescoral.oxygen.cms.api.service.CouponMarketSelectorService;
import java.util.List;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class CouponMarketSelectorPublicService implements ApiService<CouponMarketSelectorDto> {

  private final CouponMarketSelectorService couponMarketSelectorService;

  public List<CouponMarketSelectorDto> findByBrand(String brand) {
    return couponMarketSelectorService.findByBrand(brand).stream()
        .map(CouponMarketSelectorMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
