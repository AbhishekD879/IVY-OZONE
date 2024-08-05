package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.InitSignpostingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper(uses = {MapUtil.class})
public interface InitSignpostingMapper {
  InitSignpostingMapper INSTANCE = Mappers.getMapper(InitSignpostingMapper.class);

  @Mapping(
      target = "showToCustomer",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.ShowTo.class})
  @Mapping(
      target = "vipLevels",
      qualifiedBy = {MapUtil.MapUtils.class, MapUtil.EmptyList.class})
  InitSignpostingDto toDto(Promotion entity);
}
