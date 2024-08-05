package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.OfferDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Offer;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {DateMapper.class, MapUtil.class})
public interface OfferMapper {
  OfferMapper INSTANCE = Mappers.getMapper(OfferMapper.class);

  @Mapping(target = "image", source = "imageUri")
  @Mapping(
      target = "vipLevels",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.EmptyList.class})
  @Mapping(
      target = "showToCustomer",
      source = "showOfferTo",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.ShowTo.class})
  @Mapping(
      target = "module",
      expression = "java(entity.getModule() != null ? entity.getModule().toString() : null)")
  OfferDto toDto(Offer entity);
}
