package com.ladbrokescoral.oxygen.bigcompetition.mapper.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.GroupModuleDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import org.mapstruct.Mapper;
import org.mapstruct.ReportingPolicy;
import org.mapstruct.factory.Mappers;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE)
@FunctionalInterface
public interface GroupModuleDtoMapper {

  GroupModuleDtoMapper INSTANCE = Mappers.getMapper(GroupModuleDtoMapper.class);

  GroupModuleDto toDto(CompetitionModule entity);
}
