package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.InPlayConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplayConfig;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface InPlayConfigMapper {
  InPlayConfigMapper INSTANCE = Mappers.getMapper(InPlayConfigMapper.class);

  @Mapping(target = "sportId", ignore = true)
  InPlayConfigDto toDto(HomeInplayConfig entity);
}
