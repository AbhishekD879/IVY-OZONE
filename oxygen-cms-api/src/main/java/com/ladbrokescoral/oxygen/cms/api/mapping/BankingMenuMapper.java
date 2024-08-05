package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.BankingMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BankingMenu;
import com.ladbrokescoral.oxygen.cms.api.mapping.RightMenuMapUtil.LinkTitle;
import com.ladbrokescoral.oxygen.cms.api.mapping.RightMenuMapUtil.RightMenuUtils;
import com.ladbrokescoral.oxygen.cms.api.mapping.RightMenuMapUtil.ShowOnlyOnOS;
import com.ladbrokescoral.oxygen.cms.api.mapping.RightMenuMapUtil.UriLarge;
import com.ladbrokescoral.oxygen.cms.api.mapping.RightMenuMapUtil.UriMedium;
import com.ladbrokescoral.oxygen.cms.api.mapping.RightMenuMapUtil.UriSmall;
import java.util.Objects;
import org.mapstruct.AfterMapping;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.mapstruct.factory.Mappers;

@Mapper(uses = RightMenuMapUtil.class)
public interface BankingMenuMapper {

  BankingMenuMapper INSTANCE = Mappers.getMapper(BankingMenuMapper.class);

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
  BankingMenuDto toDto(BankingMenu entity);

  @AfterMapping
  default void updateRightMenu(BankingMenu entity, @MappingTarget BankingMenuDto target) {
    if (Objects.nonNull(entity.getType()) && entity.getType().equals("link")) {
      target.setTargetUri(Objects.nonNull(entity.getTargetUri()) ? entity.getTargetUri() : "");
    } else {
      target.setButtonClass(Objects.nonNull(entity.getTargetUri()) ? entity.getTargetUri() : "");
    }
  }
}
