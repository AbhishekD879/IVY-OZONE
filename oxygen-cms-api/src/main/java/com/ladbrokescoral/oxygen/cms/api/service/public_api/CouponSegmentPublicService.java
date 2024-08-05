package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.CouponSegmentDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.CouponSegmentMapper;
import com.ladbrokescoral.oxygen.cms.api.service.ApiService;
import com.ladbrokescoral.oxygen.cms.api.service.CouponSegmentService;
import java.util.List;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class CouponSegmentPublicService implements ApiService<CouponSegmentDto> {

  private final CouponSegmentService couponSegmentService;

  public List<CouponSegmentDto> findByBrand(String brand) {
    return couponSegmentService.findByBrand(brand).stream()
        .map(CouponSegmentMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
