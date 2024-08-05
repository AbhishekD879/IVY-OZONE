package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipSportCategorySvgDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {MapUtil.class})
public interface LuckyDipSportCategorySvgMapper {

  LuckyDipSportCategorySvgMapper INSTANCE = Mappers.getMapper(LuckyDipSportCategorySvgMapper.class);

  @Mapping(
      target = "ssCategoryCode",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.NullToEmpty.class})
  LuckyDipSportCategorySvgDto sportToSvg(SportCategory sportCategory);
}
