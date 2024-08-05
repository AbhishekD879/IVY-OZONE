package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.BottomMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BottomMenu;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface BottomMenuMapper {
  BottomMenuMapper INSTANCE = Mappers.getMapper(BottomMenuMapper.class);

  BottomMenuDto toDto(BottomMenu entity);
}
