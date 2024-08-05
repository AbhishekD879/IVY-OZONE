package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.QuickLinkDto;
import com.ladbrokescoral.oxygen.cms.api.entity.QuickLink;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper(uses = DateMapper.class)
public interface QuickLinkMapper {
  QuickLinkMapper INSTANCE = Mappers.getMapper(QuickLinkMapper.class);

  @Mapping(target = "iconUrl", source = "uriMedium")
  @Mapping(target = "iconLargeUrl", source = "uriLarge")
  QuickLinkDto toDto(QuickLink entity);
}
