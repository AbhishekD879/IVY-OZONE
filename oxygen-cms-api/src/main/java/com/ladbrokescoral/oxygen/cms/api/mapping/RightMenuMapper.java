package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.RightMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RightMenu;
import com.ladbrokescoral.oxygen.cms.api.mapping.RightMenuMapUtil.*;
import java.util.Objects;
import org.mapstruct.AfterMapping;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.mapstruct.factory.Mappers;

@Mapper(uses = RightMenuMapUtil.class)
public interface RightMenuMapper {
  RightMenuMapper INSTANCE = Mappers.getMapper(RightMenuMapper.class);

  @Mapping(
      target = "linkTitle",
      source = "entity",
      qualifiedBy = {RightMenuUtils.class, LinkTitle.class})
  @Mapping(
      target = "uriLarge",
      source = "entity",
      qualifiedBy = {RightMenuUtils.class, UriLarge.class})
  @Mapping(
      target = "uriMedium",
      source = "entity",
      qualifiedBy = {RightMenuUtils.class, UriMedium.class})
  @Mapping(
      target = "uriSmall",
      source = "entity",
      qualifiedBy = {RightMenuUtils.class, UriSmall.class})
  @Mapping(
      target = "showOnlyOnOS",
      source = "entity",
      qualifiedBy = {RightMenuUtils.class, ShowOnlyOnOS.class})
  @Mapping(target = "iconAlignment", source = "iconAligment")
  @Mapping(target = "buttonClass", ignore = true)
  RightMenuDto toDto(RightMenu entity);

  @AfterMapping
  default void updateRightMenu(RightMenu entity, @MappingTarget RightMenuDto target) {
    if (Objects.nonNull(entity.getType()) && entity.getType().equals("link")) {
      target.setTargetUri(Objects.nonNull(entity.getTargetUri()) ? entity.getTargetUri() : "");
    } else {
      target.setButtonClass(Objects.nonNull(entity.getTargetUri()) ? entity.getTargetUri() : "");
    }
  }
}
