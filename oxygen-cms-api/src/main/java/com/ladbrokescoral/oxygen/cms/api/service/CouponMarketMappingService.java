package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.CouponMarketMappingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.CouponMarketMappingEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.CouponMarketMappingRepository;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

/** @author PBalarangakumar 08-02-2024 */
@Service
public class CouponMarketMappingService extends SortableService<CouponMarketMappingEntity> {

  private final CouponMarketMappingRepository couponMarketMappingRepository;
  private final ModelMapper modelMapper;

  public CouponMarketMappingService(
      final CouponMarketMappingRepository couponMarketMappingRepository,
      final ModelMapper modelMapper) {
    super(couponMarketMappingRepository);

    this.couponMarketMappingRepository = couponMarketMappingRepository;
    this.modelMapper = modelMapper;
  }

  public Optional<CouponMarketMappingEntity> findByCouponId(String couponId) {

    return couponMarketMappingRepository.findByCouponId(couponId);
  }

  public List<CouponMarketMappingDto> findByBrandDto(String brand) {

    return couponMarketMappingRepository.findByBrand(brand).stream()
        .map(entity -> modelMapper.map(entity, CouponMarketMappingDto.class))
        .collect(Collectors.toList());
  }
}
