package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.model.RacingFormEvent;

public interface RacingFormEventMapper {

  public void map(EventsModuleData eventsModuleData, RacingFormEvent racingFormEvent);
}
