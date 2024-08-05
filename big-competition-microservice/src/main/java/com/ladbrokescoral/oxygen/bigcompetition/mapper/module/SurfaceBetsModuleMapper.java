package com.ladbrokescoral.oxygen.bigcompetition.mapper.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.SurfaceBetsModuleDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import org.mapstruct.Mapper;
import org.mapstruct.ReportingPolicy;
import org.mapstruct.factory.Mappers;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface SurfaceBetsModuleMapper {

  SurfaceBetsModuleMapper INSTANCE = Mappers.getMapper(SurfaceBetsModuleMapper.class);

  SurfaceBetsModuleDto toDto(CompetitionModule entity);
}
