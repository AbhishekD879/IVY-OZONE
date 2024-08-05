package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.HeaderSubMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HeaderSubMenu;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface HeaderSubMenuMapper {

  HeaderSubMenuMapper INSTANCE = Mappers.getMapper(HeaderSubMenuMapper.class);

  HeaderSubMenuDto toDto(HeaderSubMenu entity);
}
