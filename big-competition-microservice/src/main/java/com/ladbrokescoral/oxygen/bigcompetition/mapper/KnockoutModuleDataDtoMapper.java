package com.ladbrokescoral.oxygen.bigcompetition.mapper;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.knockout.CompetitionKnockoutEventDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.knockout.CompetitionKnockoutModuleDataDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.knockout.CompetitionKnockoutRoundDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionKnockoutEvent;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionKnockoutModuleData;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionKnockoutRound;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface KnockoutModuleDataDtoMapper {

  KnockoutModuleDataDtoMapper INSTANCE = Mappers.getMapper(KnockoutModuleDataDtoMapper.class);

  CompetitionKnockoutModuleDataDto toDto(CompetitionKnockoutModuleData entity);

  CompetitionKnockoutRoundDto toDto(CompetitionKnockoutRound entity);

  @Mapping(target = "obEvent", ignore = true)
  @Mapping(target = "participants", ignore = true)
  @Mapping(target = "resulted", ignore = true)
  @Mapping(target = "result", ignore = true)
  CompetitionKnockoutEventDto toDto(CompetitionKnockoutEvent entity);
}
