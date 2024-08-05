package com.ladbrokescoral.oxygen.bigcompetition.mapper.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.HighlightCarouselModuleDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import org.mapstruct.Mapper;
import org.mapstruct.ReportingPolicy;
import org.mapstruct.factory.Mappers;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface HighlightCorosolModuleMapper {

  HighlightCorosolModuleMapper INSTANCE = Mappers.getMapper(HighlightCorosolModuleMapper.class);

  HighlightCarouselModuleDto toDto(CompetitionModule entity);
}
