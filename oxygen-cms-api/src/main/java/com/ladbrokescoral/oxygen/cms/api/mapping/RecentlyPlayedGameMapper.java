package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.RecentlyPlayedGameDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface RecentlyPlayedGameMapper {

  static RecentlyPlayedGameMapper getInstance() {
    return RecentlyPlayedGameMapperInstance.RPG_INSTANCE;
  }

  RecentlyPlayedGameDto toDto(SportModule entity);

  RecentlyPlayedGameDto copy(RecentlyPlayedGameDto recentlyPlayedGameDto);

  final class RecentlyPlayedGameMapperInstance {
    private static final RecentlyPlayedGameMapper RPG_INSTANCE =
        Mappers.getMapper(RecentlyPlayedGameMapper.class);

    private RecentlyPlayedGameMapperInstance() {}
  }
}
