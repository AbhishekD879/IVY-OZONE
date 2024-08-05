package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.TopMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.TopMenu;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface TopMenuMapper {
  TopMenuMapper INSTANCE = Mappers.getMapper(TopMenuMapper.class);

  TopMenuDto toDto(TopMenu entity);
}
