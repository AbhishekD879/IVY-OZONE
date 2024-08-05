package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.RenderConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RenderConfig;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface RenderConfigMapper {

  RenderConfigMapper INSTANCE = Mappers.getMapper(RenderConfigMapper.class);

  RenderConfigDto toDto(RenderConfig source);
}
