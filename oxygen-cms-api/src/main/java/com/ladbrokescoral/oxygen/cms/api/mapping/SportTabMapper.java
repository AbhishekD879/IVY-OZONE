package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.SportTabInputDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface SportTabMapper {
  SportTabMapper INSTANCE = Mappers.getMapper(SportTabMapper.class);

  SportTab toEntity(SportTabInputDto entity);
}
