package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.egalacoral.spark.siteserver.model.Market;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeCompleteMarketDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeMarketDto;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface SiteServeMarketDtoMapper {
  SiteServeMarketDtoMapper INSTANCE = Mappers.getMapper(SiteServeMarketDtoMapper.class);

  @Mapping(target = "name", expression = "java(entity.getName().replace(\"|\", \"\"))")
  SiteServeMarketDto toDto(Market entity);

  @Mapping(target = "outcomes", ignore = true)
  @Mapping(target = "flags", ignore = true)
  SiteServeCompleteMarketDto toDtoWithoutOutcomes(Market market);
}
