package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.StaticBlockDto;
import com.ladbrokescoral.oxygen.cms.api.entity.StaticBlock;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface StaticBlockMapper {
  StaticBlockMapper INSTANCE = Mappers.getMapper(StaticBlockMapper.class);

  StaticBlockDto toDto(StaticBlock entity);
}
