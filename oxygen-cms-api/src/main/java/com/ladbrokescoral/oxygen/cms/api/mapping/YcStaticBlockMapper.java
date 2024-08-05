package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.YcStaticBlockDto;
import com.ladbrokescoral.oxygen.cms.api.entity.YourCallStaticBlock;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface YcStaticBlockMapper {
  YcStaticBlockMapper INSTANCE = Mappers.getMapper(YcStaticBlockMapper.class);

  YcStaticBlockDto toDto(YourCallStaticBlock entity);
}
