package com.ladbrokescoral.oxygen.bigcompetition.mapper.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.BybWidgetData;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.BybWidgetModuleDto;
import com.ladbrokescoral.oxygen.cms.client.model.BybWidgetDataDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import org.mapstruct.Mapper;
import org.mapstruct.ReportingPolicy;
import org.mapstruct.factory.Mappers;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface BybWidgetModuleDtoMapper {

  BybWidgetModuleDtoMapper INSTANCE = Mappers.getMapper(BybWidgetModuleDtoMapper.class);

  BybWidgetModuleDto toDto(CompetitionModule entity);

  BybWidgetData toDto(BybWidgetDataDto bybWidgetDataDto);
}
