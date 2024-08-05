package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.model.RacingFormEvent;
import org.springframework.util.ObjectUtils;

public class SimpleRacingFormEventMapper implements RacingFormEventMapper {

  public static final String EMPTY_STRING = "";

  @Override
  public void map(EventsModuleData eventsModuleData, RacingFormEvent rfe) {
    String distance = rfe.getDistance();
    String goingCode = rfe.getGoing();
    if (!ObjectUtils.isEmpty(distance) || !ObjectUtils.isEmpty(goingCode)) {
      com.coral.oxygen.middleware.pojos.model.output.RacingFormEvent racingFormEvent =
          new com.coral.oxygen.middleware.pojos.model.output.RacingFormEvent();
      racingFormEvent.setDistance(ObjectUtils.isEmpty(distance) ? EMPTY_STRING : distance);
      racingFormEvent.setGoing(ObjectUtils.isEmpty(goingCode) ? EMPTY_STRING : goingCode);
      eventsModuleData.setRacingFormEvent(racingFormEvent);
    }
  }
}
