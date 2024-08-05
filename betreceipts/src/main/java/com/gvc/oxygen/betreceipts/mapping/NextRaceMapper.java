package com.gvc.oxygen.betreceipts.mapping;

import com.egalacoral.spark.siteserver.model.Event;
import com.gvc.oxygen.betreceipts.dto.RaceDTO;
import com.gvc.oxygen.betreceipts.entity.NextRace;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Component;

@Component
@Data
@AllArgsConstructor
public class NextRaceMapper {

  private final ModelMapper modelMapper;

  public NextRace toDto(Event entity) {
    return modelMapper.map(entity, NextRace.class);
  }

  public NextRace toDto(Event entity, RaceDTO raceEvent) {
    raceEvent.setId(entity.getId());
    NextRace nextRace = modelMapper.map(entity, NextRace.class);
    modelMapper.map(raceEvent, nextRace);
    return nextRace;
  }
}
