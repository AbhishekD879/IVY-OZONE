package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.TopGameDto;
import com.ladbrokescoral.oxygen.cms.api.entity.TopGame;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {MapUtil.class})
public interface TopGameMapper {
  TopGameMapper INSTANCE = Mappers.getMapper(TopGameMapper.class);

  @Mapping(
      target = "uriSmall",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "uriMedium",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "uriLarge",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "uriSmallIcon",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "uriMediumIcon",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(
      target = "uriLargeIcon",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(target = "filename", source = "entity.filename.filename")
  TopGameDto toDto(TopGame entity);
}
