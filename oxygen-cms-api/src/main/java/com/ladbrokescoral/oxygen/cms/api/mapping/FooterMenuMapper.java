package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.*;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import com.ladbrokescoral.oxygen.cms.api.mapping.FooterMenuMapUtil.*;
import com.ladbrokescoral.oxygen.cms.api.mapping.MapUtil.MapUtils;
import com.ladbrokescoral.oxygen.cms.api.mapping.MapUtil.NullToEmpty;
import com.ladbrokescoral.oxygen.cms.api.mapping.MapUtil.NullToNull;
import com.ladbrokescoral.oxygen.cms.api.mapping.MapUtil.UriSubstring;
import java.util.List;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {MapUtil.class, FooterMenuMapUtil.class})
public interface FooterMenuMapper extends SegmentReferenceMapper {
  FooterMenuMapper INSTANCE = Mappers.getMapper(FooterMenuMapper.class);

  @Mapping(
      target = "uriSmall",
      qualifiedBy = {MapUtils.class, UriSubstring.class})
  @Mapping(
      target = "uriLarge",
      qualifiedBy = {MapUtils.class, UriSubstring.class})
  @Mapping(
      target = "targetUri",
      qualifiedBy = {MapUtils.class, NullToEmpty.class})
  @Mapping(
      target = "linkTitle",
      qualifiedBy = {MapUtils.class, NullToEmpty.class})
  @Mapping(
      target = "svg",
      qualifiedBy = {MapUtils.class, NullToNull.class})
  @Mapping(
      target = "svgId",
      qualifiedBy = {MapUtils.class, NullToNull.class})
  FooterMenuV2Dto toDtoV2(FooterMenu entity);

  @Mapping(
      target = "target",
      source = "entity",
      qualifiedBy = {FooterMenuMapUtils.class, ToTarget.class})
  @Mapping(
      target = "title",
      source = "linkTitle",
      qualifiedBy = {MapUtils.class, NullToEmpty.class})
  @Mapping(
      target = "image",
      source = "uriSmall",
      qualifiedBy = {MapUtils.class, UriSubstring.class})
  @Mapping(
      target = "imageLarge",
      source = "uriLarge",
      qualifiedBy = {MapUtils.class, UriSubstring.class})
  @Mapping(
      target = "inApp",
      source = "entity",
      qualifiedBy = {FooterMenuMapUtils.class, ToInApp.class})
  @Mapping(
      target = "widget",
      source = "entity",
      qualifiedBy = {FooterMenuMapUtils.class, ToWidget.class})
  @Mapping(
      target = "svg",
      qualifiedBy = {MapUtils.class, NullToNull.class})
  @Mapping(
      target = "svgId",
      qualifiedBy = {MapUtils.class, NullToNull.class})
  @Mapping(
      target = "device",
      source = "entity",
      qualifiedBy = {FooterMenuMapUtils.class, ToDevice.class})
  FooterMenuV3Dto toDtoV3(FooterMenu entity);

  @Mapping(
      target = "targetUri",
      qualifiedBy = {MapUtils.class, NullToEmpty.class})
  @Mapping(
      target = "linkTitle",
      qualifiedBy = {MapUtils.class, NullToEmpty.class})
  @Mapping(
      target = "svgId",
      qualifiedBy = {MapUtils.class, NullToNull.class})
  InitialDataFooterMenuV2Dto toInitialDtoV2(FooterMenu footerMenu);

  @Mapping(target = "segmentReferences", ignore = true)
  @Mapping(target = "segments", ignore = true)
  FooterMenuSegmentedDto toSegmentedDto(FooterMenu entity);

  default FooterMenuSegmentedDto toSegmentedDto(FooterMenu entity, List<String> segments) {
    FooterMenuSegmentedDto footerMenuSegmentedDto = toSegmentedDto(entity);
    footerMenuSegmentedDto.setSegments(getSegments(entity, segments));
    footerMenuSegmentedDto.setSegmentReferences(getSegmentReferences(entity));
    return footerMenuSegmentedDto;
  }
}
