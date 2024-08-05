package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.HeaderMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HeaderMenu;
import java.util.List;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface HeaderMenuMapper {
  HeaderMenuMapper INSTANCE = Mappers.getMapper(HeaderMenuMapper.class);

  @Mapping(target = "children", source = "childrenList")
  HeaderMenuDto toDto(HeaderMenu entity, List<HeaderMenu> childrenList);
}
