package com.ladbrokescoral.oxygen.bigcompetition.mapper.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.AemModuleDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import org.mapstruct.Mapper;
import org.mapstruct.ReportingPolicy;
import org.mapstruct.factory.Mappers;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE)
@FunctionalInterface
public interface AemModuleDtoMapper {

  AemModuleDtoMapper INSTANCE = Mappers.getMapper(AemModuleDtoMapper.class);

  AemModuleDto toDto(CompetitionModule entity);
}
