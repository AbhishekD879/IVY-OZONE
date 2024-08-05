package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.model.Event;

public class EventNameInplayMapper extends ChainedEventMapper {

  public EventNameInplayMapper(EventMapper chain) {
    super(chain);
  }

  @Override
  protected void populate(EventsModuleData outputEvent, Event event) {
    outputEvent.setName(calculateEventName(outputEvent));
  }

  private String calculateEventName(EventsModuleData outputEvent) {
    return outputEvent.getNameOverride() == null
        ? outputEvent.getName()
        : outputEvent.getNameOverride();
  }
}
