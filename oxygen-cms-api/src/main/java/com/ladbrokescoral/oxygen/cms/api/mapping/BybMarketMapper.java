package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.BybMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybMarket;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface BybMarketMapper {

  BybMarketMapper INSTANCE = Mappers.getMapper(BybMarketMapper.class);

  BybMarketDto toDto(BybMarket entity);
}
