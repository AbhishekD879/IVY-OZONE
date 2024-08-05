package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.HeaderContactMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HeaderContactMenu;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface HeaderContactMenuMapper {
  HeaderContactMenuMapper INSTANCE = Mappers.getMapper(HeaderContactMenuMapper.class);

  HeaderContactMenuDto toDto(HeaderContactMenu entity);
}
