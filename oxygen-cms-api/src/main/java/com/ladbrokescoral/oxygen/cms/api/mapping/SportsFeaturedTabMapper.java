package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.SportsFeaturedTabDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportsFeaturedTab;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface SportsFeaturedTabMapper {
  SportsFeaturedTabMapper INSTANCE = Mappers.getMapper(SportsFeaturedTabMapper.class);

  SportsFeaturedTabDto toDto(SportsFeaturedTab sportsFeaturedTab);
}
