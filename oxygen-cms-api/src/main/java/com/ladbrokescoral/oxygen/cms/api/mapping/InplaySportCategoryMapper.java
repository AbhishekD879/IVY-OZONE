package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.InplaySportCategoryDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Sport;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {MapUtil.class})
public interface InplaySportCategoryMapper {

  InplaySportCategoryMapper INSTANCE = Mappers.getMapper(InplaySportCategoryMapper.class);

  @Mapping(
      target = "ssCategoryCode",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.NullToEmpty.class})
  @Mapping(target = "scoreBoardUrl", source = "scoreBoardUri")
  InplaySportCategoryDto categoryToInplay(SportCategory sportCategory);

  @Mapping(
      target = "ssCategoryCode",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.NullToEmpty.class})
  InplaySportCategoryDto sportToInplay(Sport sport);
}
