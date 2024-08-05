package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.BannerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Banner;
import com.ladbrokescoral.oxygen.cms.api.mapping.MapUtil.EmptyList;
import com.ladbrokescoral.oxygen.cms.api.mapping.MapUtil.MapUtils;
import com.ladbrokescoral.oxygen.cms.api.mapping.MapUtil.ShowTo;
import com.ladbrokescoral.oxygen.cms.api.mapping.MapUtil.UriSubstring;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {MapUtil.class, DateMapper.class})
public interface BannerMapper {
  BannerMapper INSTANCE = Mappers.getMapper(BannerMapper.class);

  @Mapping(target = "filename", source = "entity.filename.filename")
  @Mapping(target = "desktopFilename", source = "entity.desktopFilename.filename")
  @Mapping(
      target = "uriMedium",
      qualifiedBy = {MapUtils.class, UriSubstring.class})
  @Mapping(
      target = "uriSmall",
      qualifiedBy = {MapUtils.class, UriSubstring.class})
  @Mapping(
      target = "desktopUriMedium",
      qualifiedBy = {MapUtils.class, UriSubstring.class})
  @Mapping(
      target = "desktopUriSmall",
      qualifiedBy = {MapUtils.class, UriSubstring.class})
  @Mapping(
      target = "showToCustomer",
      qualifiedBy = {MapUtils.class, ShowTo.class})
  @Mapping(
      target = "vipLevels",
      qualifiedBy = {MapUtils.class, EmptyList.class})
  BannerDto toDto(Banner entity);
}
