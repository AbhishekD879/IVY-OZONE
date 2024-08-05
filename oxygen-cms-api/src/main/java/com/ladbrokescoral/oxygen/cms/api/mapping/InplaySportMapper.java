package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.InplaySportDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplaySport;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface InplaySportMapper {
  InplaySportMapper INSTANCE = Mappers.getMapper(InplaySportMapper.class);

  InplaySportDto toDto(HomeInplaySport entity);
}
