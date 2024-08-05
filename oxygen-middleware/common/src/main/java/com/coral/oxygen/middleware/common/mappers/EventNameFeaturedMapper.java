package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.model.Event;

/** Created by azayats on 12.01.17. */
public class EventNameFeaturedMapper extends ChainedEventMapper {

  public EventNameFeaturedMapper(EventMapper chain) {
    super(chain);
  }

  @Override
  protected void populate(EventsModuleData outputEvent, Event event) {
    outputEvent.setSsName(outputEvent.getName());
    outputEvent.setName(calculateEventName(outputEvent));
  }

  private String calculateEventName(EventsModuleData outputEvent) {
    return outputEvent.getNameOverride() == null
        ? outputEvent.getName()
        : outputEvent.getNameOverride();
  }
}
