package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.CouponMarketSelectorDto;
import com.ladbrokescoral.oxygen.cms.api.entity.CouponMarketSelector;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface CouponMarketSelectorMapper {
  CouponMarketSelectorMapper INSTANCE = Mappers.getMapper(CouponMarketSelectorMapper.class);

  CouponMarketSelectorDto toDto(CouponMarketSelector entity);
}
