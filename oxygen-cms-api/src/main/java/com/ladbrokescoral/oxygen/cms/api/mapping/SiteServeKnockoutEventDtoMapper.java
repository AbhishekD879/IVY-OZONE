package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeKnockoutEventDto;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface SiteServeKnockoutEventDtoMapper {

  SiteServeKnockoutEventDtoMapper INSTANCE =
      Mappers.getMapper(SiteServeKnockoutEventDtoMapper.class);

  @Mapping(
      target = "homeTeam",
      expression =
          "java(com.ladbrokescoral.oxygen.cms.util.SiteServeUtil.getHomeTeamFromEventName(entity.getName()))")
  @Mapping(
      target = "awayTeam",
      expression =
          "java(com.ladbrokescoral.oxygen.cms.util.SiteServeUtil.getAwayTeamFromEventName(entity.getName()))")
  @Mapping(target = "eventName", expression = "java(entity.getName().replace(\"|\", \"\"))")
  SiteServeKnockoutEventDto toDto(Event entity);
}
