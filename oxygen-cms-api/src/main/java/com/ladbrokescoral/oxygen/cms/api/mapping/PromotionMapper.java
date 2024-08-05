package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.PromotionDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PromotionV2Dto;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {MapUtil.class, DateMapper.class})
public interface PromotionMapper {

  PromotionMapper INSTANCE = Mappers.getMapper(PromotionMapper.class);

  @Mapping(
      target = "uriMedium",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(target = "filename", source = "entity.filename.filename")
  @Mapping(
      target = "showToCustomer",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.ShowTo.class})
  @Mapping(
      target = "vipLevels",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.EmptyList.class})
  @Mapping(
      target = "categoryId",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.ObjectIdListToStringList.class})
  PromotionDto toDto(Promotion entity);

  @Mapping(
      target = "uriMedium",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.UriSubstring.class})
  @Mapping(target = "filename", source = "entity.filename.filename")
  @Mapping(
      target = "showToCustomer",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.ShowTo.class})
  @Mapping(
      target = "vipLevels",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.EmptyList.class})
  PromotionV2Dto toDtoV2(Promotion entity);
}
