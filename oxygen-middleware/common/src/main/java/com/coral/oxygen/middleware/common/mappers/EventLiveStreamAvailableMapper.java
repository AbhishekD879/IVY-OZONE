package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.common.utils.EventLiveStreamMapperUtil;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.egalacoral.spark.siteserver.model.Event;

public class EventLiveStreamAvailableMapper extends ChainedEventMapper {

  public EventLiveStreamAvailableMapper(EventMapper chain) {
    super(chain);
  }

  @Override
  protected void populate(EventsModuleData result, Event event) {
    result.setLiveStreamAvailable(EventLiveStreamMapperUtil.isLiveStreamAvailable(event));
  }
}
