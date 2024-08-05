package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.TeamDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Team;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface TeamMapper {
  static TeamMapper getInstance() {
    return TeamMapperInstance.TEAM_MAPPER_INSTANCE;
  }

  TeamDto toDto(Team team);

  final class TeamMapperInstance {
    private static final TeamMapper TEAM_MAPPER_INSTANCE = Mappers.getMapper(TeamMapper.class);

    private TeamMapperInstance() {}
  }
}
