package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.YcLeagueDto;
import com.ladbrokescoral.oxygen.cms.api.entity.YourCallLeague;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface YcLeagueMapper {
  YcLeagueMapper INSTANCE = Mappers.getMapper(YcLeagueMapper.class);

  YcLeagueDto toDto(YourCallLeague entity);
}
