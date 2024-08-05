package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.RacingModuleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface RacingModuleMapper {

  @Mapping(target = "title", source = "entity.title")
  @Mapping(target = "active", expression = "java(!entity.isDisabled())")
  RacingModuleDto toDto(SportModule entity);
}
