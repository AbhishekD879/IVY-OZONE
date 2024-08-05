package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.egalacoral.spark.siteserver.model.Outcome;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeCompleteOutcomeDto;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface SiteServeOutcomeDtoMapper {

  @Mapping(target = "prices", ignore = true)
  SiteServeCompleteOutcomeDto toDtoWithoutPrices(Outcome outcome);

  @NoArgsConstructor(access = AccessLevel.PRIVATE)
  class SiteServeOutcomeDtoMapperInstance {
    public static final SiteServeOutcomeDtoMapper INSTANCE =
        Mappers.getMapper(SiteServeOutcomeDtoMapper.class);
  }
}
