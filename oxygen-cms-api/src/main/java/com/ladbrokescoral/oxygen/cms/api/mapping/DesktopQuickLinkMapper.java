package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.DesktopQuickLinkDto;
import com.ladbrokescoral.oxygen.cms.api.entity.DesktopQuickLink;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface DesktopQuickLinkMapper {
  DesktopQuickLinkMapper INSTANCE = Mappers.getMapper(DesktopQuickLinkMapper.class);

  DesktopQuickLinkDto toDto(DesktopQuickLink entity);
}
