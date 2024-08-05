package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeCompleteEventDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventExtendedDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventTreeNodeDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventWithSiteChannels;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeMinimalEventDto;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;
import org.springframework.util.StringUtils;

@Mapper
public interface SiteServeEventDtoMapper {

  SiteServeEventDtoMapper INSTANCE = Mappers.getMapper(SiteServeEventDtoMapper.class);

  @Mapping(target = "marketCount", ignore = true)
  SiteServeEventDto toDto(SiteServeEventExtendedDto entity);

  @Mapping(target = "nameOverride", source = "entity.name")
  @Mapping(target = "outright", ignore = true)
  @Mapping(target = "templateMarketName", expression = "java(this.getMarketTemplateName(entity))")
  SiteServeEventExtendedDto toDto(Event entity);

  @Mapping(target = "name", expression = "java(entity.getName().replace(\"|\", \"\"))")
  SiteServeMinimalEventDto toMinimalDto(Event entity);

  @Mapping(target = "nameOverride", expression = "java(this.getNameOverride(entity))")
  @Mapping(target = "outright", ignore = true)
  @Mapping(target = "templateMarketName", ignore = true)
  SiteServeEventExtendedDto toDtoSelection(Event entity);

  @Mapping(target = "nameOverride", source = "entity.name")
  @Mapping(target = "outright", ignore = true)
  @Mapping(target = "templateMarketName", expression = "java(this.getMarketTemplateName(entity))")
  SiteServeEventWithSiteChannels toDtoWithChannels(Event entity);

  SiteServeEventExtendedDto toDtoWithoutChannels(SiteServeEventWithSiteChannels entity);

  SiteServeEventTreeNodeDto toDtoNode(Event entity);

  @Mapping(target = "eventIsLive", source = "isLiveNowEvent")
  @Mapping(target = "markets", ignore = true)
  @Mapping(target = "eventFlagCodes", ignore = true)
  SiteServeCompleteEventDto toDtoWithoutMarkets(Event entity);

  default String getNameOverride(Event entity) {
    return entity.getMarkets().stream()
        .map(Market::getOutcomes)
        .filter(outcomes -> !outcomes.isEmpty())
        .map(outcomes -> outcomes.get(0).getName())
        .findFirst()
        .orElse("");
  }

  default String getMarketTemplateName(Event event) {
    return event.getMarkets().stream()
        .map(Market::getTemplateMarketName)
        .filter(templateName -> !StringUtils.isEmpty(templateName))
        .findFirst()
        .orElse("");
  }
}
