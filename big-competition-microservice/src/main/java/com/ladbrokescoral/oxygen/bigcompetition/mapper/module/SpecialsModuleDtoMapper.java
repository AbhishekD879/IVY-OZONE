package com.ladbrokescoral.oxygen.bigcompetition.mapper.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.SpecialsModuleDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.ReportingPolicy;
import org.mapstruct.factory.Mappers;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE)
@FunctionalInterface
public interface SpecialsModuleDtoMapper {

  SpecialsModuleDtoMapper INSTANCE = Mappers.getMapper(SpecialsModuleDtoMapper.class);

  @Mapping(target = "linkUrl", expression = "java(entity.getSpecialModuleData().getLinkUrl())")
  SpecialsModuleDto toDto(CompetitionModule entity);
}
