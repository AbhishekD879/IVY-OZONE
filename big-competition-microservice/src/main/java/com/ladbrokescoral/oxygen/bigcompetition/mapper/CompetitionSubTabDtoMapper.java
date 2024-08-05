package com.ladbrokescoral.oxygen.bigcompetition.mapper;

import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionSubTabDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionSubTab;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
@FunctionalInterface
public interface CompetitionSubTabDtoMapper {

  CompetitionSubTabDtoMapper INSTANCE = Mappers.getMapper(CompetitionSubTabDtoMapper.class);

  @Mapping(target = "competitionModules", ignore = true)
  CompetitionSubTabDto toDto(CompetitionSubTab entity);
}
