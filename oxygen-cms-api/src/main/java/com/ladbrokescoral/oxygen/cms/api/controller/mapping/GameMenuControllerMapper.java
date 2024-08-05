package com.ladbrokescoral.oxygen.cms.api.controller.mapping;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.GameMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.GameMenu;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface GameMenuControllerMapper {

  GameMenuControllerMapper INSTANCE = Mappers.getMapper(GameMenuControllerMapper.class);

  GameMenu toEntity(GameMenuDto entity);
}
