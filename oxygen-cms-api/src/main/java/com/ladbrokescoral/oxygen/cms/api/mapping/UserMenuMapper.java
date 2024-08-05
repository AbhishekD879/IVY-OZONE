package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.UserMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.UserMenu;
import com.ladbrokescoral.oxygen.cms.api.mapping.UserMenuMapperUtil.TargetUri;
import com.ladbrokescoral.oxygen.cms.api.mapping.UserMenuMapperUtil.UriMedium;
import com.ladbrokescoral.oxygen.cms.api.mapping.UserMenuMapperUtil.UriSmall;
import com.ladbrokescoral.oxygen.cms.api.mapping.UserMenuMapperUtil.UserMenuUtils;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {MapUtil.class, UserMenuMapperUtil.class})
public interface UserMenuMapper {
  UserMenuMapper INSTANCE = Mappers.getMapper(UserMenuMapper.class);

  @Mapping(
      target = "targetUri",
      qualifiedBy = {UserMenuUtils.class, TargetUri.class})
  @Mapping(
      target = "linkTitle",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.NullToEmpty.class})
  @Mapping(
      target = "uriMedium",
      qualifiedBy = {UserMenuUtils.class, UriMedium.class})
  @Mapping(
      target = "uriSmall",
      qualifiedBy = {UserMenuUtils.class, UriSmall.class})
  UserMenuDto toDto(UserMenu entity);
}
