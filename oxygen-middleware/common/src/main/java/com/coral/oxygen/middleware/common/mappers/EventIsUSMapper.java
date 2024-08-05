package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.model.Event;

public class EventIsUSMapper extends ChainedEventMapper {

  public EventIsUSMapper(EventMapper chain) {
    super(chain);
  }

  @Override
  protected void populate(EventsModuleData result, Event event) {
    result.setUS(calculateIsUS(event));
  }

  public static boolean calculateIsUS(Event event) {
    return event.getTypeFlagCodes() != null && event.getTypeFlagCodes().contains("US");
  }
}
