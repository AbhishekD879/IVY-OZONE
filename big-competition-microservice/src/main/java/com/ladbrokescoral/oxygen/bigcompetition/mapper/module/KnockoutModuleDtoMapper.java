package com.ladbrokescoral.oxygen.bigcompetition.mapper.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.KnockoutModuleDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import org.mapstruct.Mapper;
import org.mapstruct.ReportingPolicy;
import org.mapstruct.factory.Mappers;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE)
@FunctionalInterface
public interface KnockoutModuleDtoMapper {

  KnockoutModuleDtoMapper INSTANCE = Mappers.getMapper(KnockoutModuleDtoMapper.class);

  KnockoutModuleDto toDto(CompetitionModule entity);
}
