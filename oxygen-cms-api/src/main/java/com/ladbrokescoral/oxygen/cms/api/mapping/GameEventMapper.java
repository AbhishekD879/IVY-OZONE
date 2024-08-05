package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.GameEventDto;
import com.ladbrokescoral.oxygen.cms.api.entity.GameEvent;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface GameEventMapper {
  static GameEventMapper getInstance() {
    return GameEventMapperInstance.GAME_EVENT_MAPPER_INSTANCE;
  }

  GameEventDto toDto(GameEvent gameEvent);

  final class GameEventMapperInstance {
    private static final GameEventMapper GAME_EVENT_MAPPER_INSTANCE =
        Mappers.getMapper(GameEventMapper.class);

    private GameEventMapperInstance() {}
  }
}
