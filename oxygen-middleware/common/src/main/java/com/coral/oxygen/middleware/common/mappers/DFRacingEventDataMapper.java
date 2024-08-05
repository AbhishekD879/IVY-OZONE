package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.df.RaceEvent;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.RacingFormEvent;
import org.springframework.stereotype.Component;
import org.springframework.util.ObjectUtils;

@Component
public class DFRacingEventDataMapper {

  public static final String EMPTY_STRING = "";

  public void map(EventsModuleData d, RaceEvent raceEvent) {
    Integer distance = raceEvent.getYards();
    String goingCode = raceEvent.getGoingCode();
    if (!ObjectUtils.isEmpty(distance) || !ObjectUtils.isEmpty(goingCode)) {
      RacingFormEvent racingFormEvent = new RacingFormEvent();
      racingFormEvent.setDistance(
          ObjectUtils.isEmpty(distance) ? EMPTY_STRING : String.valueOf(distance));
      racingFormEvent.setGoing(ObjectUtils.isEmpty(goingCode) ? EMPTY_STRING : goingCode);
      d.setRacingFormEvent(racingFormEvent);
    }
  }
}
