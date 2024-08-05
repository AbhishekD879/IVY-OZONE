package com.ladbrokescoral.oxygen.bigcompetition.mapper.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.NextEventsModuleDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import org.mapstruct.Mapper;
import org.mapstruct.ReportingPolicy;
import org.mapstruct.factory.Mappers;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE)
@FunctionalInterface
public interface NextEventsModuleDtoMapper {

  NextEventsModuleDtoMapper INSTANCE = Mappers.getMapper(NextEventsModuleDtoMapper.class);

  NextEventsModuleDto toDto(CompetitionModule entity);
}
