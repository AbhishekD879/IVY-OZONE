package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.LeagueDto;
import com.ladbrokescoral.oxygen.cms.api.entity.League;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface LeagueMapper {
  LeagueMapper INSTANCE = Mappers.getMapper(LeagueMapper.class);

  LeagueDto toDto(League entity);
}
