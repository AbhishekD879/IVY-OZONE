package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.CouponSegmentDto;
import com.ladbrokescoral.oxygen.cms.api.entity.CouponSegment;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface CouponSegmentMapper {
  CouponSegmentMapper INSTANCE = Mappers.getMapper(CouponSegmentMapper.class);

  CouponSegmentDto toDto(CouponSegment entity);
}
