package com.ladbrokescoral.oxygen.cms.api.controller.mapping;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.RacingEdpMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RacingEdpMarket;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface RacingEdpMarketsMapper {

  RacingEdpMarketsMapper ENTITY_MAPPER = Mappers.getMapper(RacingEdpMarketsMapper.class);

  @Mapping(target = "createdBy", ignore = true)
  @Mapping(target = "createdByUserName", ignore = true)
  @Mapping(target = "updatedBy", ignore = true)
  @Mapping(target = "updatedByUserName", ignore = true)
  @Mapping(target = "createdAt", ignore = true)
  @Mapping(target = "updatedAt", ignore = true)
  RacingEdpMarket toEntity(RacingEdpMarketDto dto);

  RacingEdpMarketDto toDto(RacingEdpMarket entity);
}
