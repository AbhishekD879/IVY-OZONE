package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.TeamBetsDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface TeamBetsMapper {
  TeamBetsMapper INSTANCE = Mappers.getMapper(TeamBetsMapper.class);

  @Mapping(target = "noOfMaxSelections", source = "entity.teamAndFansBetsConfig.noOfMaxSelections")
  @Mapping(target = "enableBackedTimes", source = "entity.teamAndFansBetsConfig.enableBackedTimes")
  TeamBetsDto toDto(SportModule entity);
}
