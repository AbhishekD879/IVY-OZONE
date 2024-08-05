package com.ladbrokescoral.oxygen.bigcompetition.mapper;

import com.ladbrokescoral.oxygen.bigcompetition.dto.ParticipantDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionParticipant;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
@FunctionalInterface
public interface ParticipantDtoMapper {

  ParticipantDtoMapper INSTANCE = Mappers.getMapper(ParticipantDtoMapper.class);

  @Mapping(
      target = "name",
      expression = "java(com.ladbrokescoral.oxygen.bigcompetition.util.Utils.buildName(entity))")
  @Mapping(
      target = "abbreviation",
      expression =
          "java(com.ladbrokescoral.oxygen.bigcompetition.util.Utils.buildAbbreviation(entity))")
  @Mapping(target = "obName", ignore = true)
  @Mapping(target = "isWinner", ignore = true)
  ParticipantDto toDto(CompetitionParticipant entity);
}
