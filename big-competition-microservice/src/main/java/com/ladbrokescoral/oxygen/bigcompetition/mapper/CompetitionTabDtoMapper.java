package com.ladbrokescoral.oxygen.bigcompetition.mapper;

import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionTabDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionTab;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
@FunctionalInterface
public interface CompetitionTabDtoMapper {

  CompetitionTabDtoMapper INSTANCE = Mappers.getMapper(CompetitionTabDtoMapper.class);

  @Mapping(target = "title", source = "entity.name")
  @Mapping(target = "competitionSubTabs", ignore = true)
  @Mapping(target = "competitionModules", ignore = true)
  CompetitionTabDto toDto(CompetitionTab entity);
}
