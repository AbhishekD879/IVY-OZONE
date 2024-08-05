package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.coral.oxygen.df.model.RaceEvent;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.entity.NextRace;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface NextRaceMapper {

  NextRaceMapper INSTANCE = Mappers.getMapper(NextRaceMapper.class);

  NextRace toDto(Event entity);

  NextRace toDto(Event entity, RaceEvent raceEvent);
}
