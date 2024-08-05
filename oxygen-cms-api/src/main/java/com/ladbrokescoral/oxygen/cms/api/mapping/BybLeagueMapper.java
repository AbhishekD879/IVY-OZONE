package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.BybLeagueDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybLeague;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface BybLeagueMapper {
  BybLeagueMapper INSTANCE = Mappers.getMapper(BybLeagueMapper.class);

  BybLeagueDto toDto(BybLeague entity);
}
