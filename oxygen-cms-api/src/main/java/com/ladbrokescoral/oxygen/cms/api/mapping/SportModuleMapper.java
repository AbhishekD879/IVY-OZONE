package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.SportModuleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface SportModuleMapper {
  SportModuleMapper INSTANCE = Mappers.getMapper(SportModuleMapper.class);

  SportModuleDto toDto(SportModule entity);

  SportModuleDto copy(SportModuleDto module);
}
