package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.GameMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.GameMenu;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface GameMenuMapper {

  GameMenuMapper INSTANCE = Mappers.getMapper(GameMenuMapper.class);

  GameMenuDto toDto(GameMenu entity);
}
