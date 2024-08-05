package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.model.output.OutputEvent;
import com.egalacoral.spark.siteserver.model.Event;

public class EventIsUSMapper extends ChainedEventMapper {

  public EventIsUSMapper(EventMapper chain) {
    super(chain);
  }

  @Override
  protected void populate(OutputEvent result, Event event) {
    result.setIsUS(calculateIsUS(event));
  }

  public static boolean calculateIsUS(Event event) {
    return event.getTypeFlagCodes() != null //
        && event.getTypeFlagCodes().contains("US");
  }
}
