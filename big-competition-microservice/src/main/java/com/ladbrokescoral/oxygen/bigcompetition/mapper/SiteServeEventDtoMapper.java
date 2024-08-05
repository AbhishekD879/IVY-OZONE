package com.ladbrokescoral.oxygen.bigcompetition.mapper;

import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.egalacoral.spark.siteserver.model.Price;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.MarketDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.OutcomeDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.PriceDto;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface SiteServeEventDtoMapper {

  SiteServeEventDtoMapper INSTANCE = Mappers.getMapper(SiteServeEventDtoMapper.class);

  @Mapping(target = "marketsCount", ignore = true)
  @Mapping(target = "participants", ignore = true)
  EventDto toDto(Event entity);

  MarketDto toDto(Market entity);

  @Mapping(target = "participants", ignore = true)
  OutcomeDto toDto(Outcome outcome);

  PriceDto toDto(Price price);
}
