package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.ConnectMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ConnectMenu;
import java.util.List;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {MapUtil.class})
public interface ConnectMenuMapper {
  ConnectMenuMapper INSTANCE = Mappers.getMapper(ConnectMenuMapper.class);

  @Mapping(
      target = "linkSubtitle",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.NullToEmpty.class})
  @Mapping(target = "children", source = "childrenList")
  ConnectMenuDto toDto(ConnectMenu entity, List<ConnectMenu> childrenList);
}
