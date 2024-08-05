package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.model.output.OutputEvent;
import com.egalacoral.spark.siteserver.model.Event;

public class EventIsLiveMapper extends ChainedEventMapper {

  public EventIsLiveMapper(EventMapper chain) {
    super(chain);
  }

  @Override
  protected void populate(OutputEvent result, Event event) {
    result.setEventIsLive(calculateEventIsLive(event));
  }

  private boolean calculateEventIsLive(Event event) {
    return "Y".equals(event.getRawIsOffCode())
        || ("-".equals(event.getRawIsOffCode()) && Boolean.TRUE.equals(event.getIsStarted()));
  }
}
