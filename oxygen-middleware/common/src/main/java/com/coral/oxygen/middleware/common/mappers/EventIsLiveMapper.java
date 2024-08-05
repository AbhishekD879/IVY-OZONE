package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.model.Event;

public class EventIsLiveMapper extends ChainedEventMapper {

  public EventIsLiveMapper(EventMapper chain) {
    super(chain);
  }

  @Override
  protected void populate(EventsModuleData result, Event event) {
    result.setEventIsLive(calculateEventIsLive(event));
  }

  private boolean calculateEventIsLive(Event event) {
    return "Y".equals(event.getRawIsOffCode())
        || ("-".equals(event.getRawIsOffCode()) && Boolean.TRUE.equals(event.getIsStarted()));
  }
}
