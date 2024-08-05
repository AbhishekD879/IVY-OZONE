package com.ladbrokescoral.oxygen.bigcompetition.mapper;

import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionDto;
import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
@FunctionalInterface
public interface CompetitionDtoMapper {

  CompetitionDtoMapper INSTANCE = Mappers.getMapper(CompetitionDtoMapper.class);

  @Mapping(target = "competitionTabs", ignore = true)
  CompetitionDto toDto(Competition entity);
}
