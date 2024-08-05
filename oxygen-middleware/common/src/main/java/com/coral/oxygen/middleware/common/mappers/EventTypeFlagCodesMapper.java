package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.model.Event;

public class EventTypeFlagCodesMapper extends ChainedEventMapper {

  public EventTypeFlagCodesMapper(EventMapper chain) {
    super(chain);
  }

  @Override
  protected void populate(EventsModuleData result, Event event) {
    result.setTypeFlagCodes(result.isLiveStreamAvailable() ? event.getTypeFlagCodes() : null);
  }
}
