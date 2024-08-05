package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.EdpMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.EdpMarket;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface EdpMarketMapper {
  EdpMarketMapper INSTANCE = Mappers.getMapper(EdpMarketMapper.class);

  EdpMarketDto toDto(EdpMarket entity);
}
