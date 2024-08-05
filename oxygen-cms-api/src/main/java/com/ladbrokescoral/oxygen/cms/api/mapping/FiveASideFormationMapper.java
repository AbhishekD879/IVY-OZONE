package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.FiveASideFormationDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FiveASideFormation;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface FiveASideFormationMapper {

  FiveASideFormationMapper INSTANCE = Mappers.getMapper(FiveASideFormationMapper.class);

  FiveASideFormationDto toDto(FiveASideFormation entity);
}
