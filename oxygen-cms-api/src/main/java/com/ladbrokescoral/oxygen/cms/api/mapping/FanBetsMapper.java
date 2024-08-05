package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.FanBetsDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface FanBetsMapper {
  FanBetsMapper INSTANCE = Mappers.getMapper(FanBetsMapper.class);

  @Mapping(target = "noOfMaxSelections", source = "entity.teamAndFansBetsConfig.noOfMaxSelections")
  @Mapping(target = "enableBackedTimes", source = "entity.teamAndFansBetsConfig.enableBackedTimes")
  FanBetsDto toDto(SportModule entity);
}
